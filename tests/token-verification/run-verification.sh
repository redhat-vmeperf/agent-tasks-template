#!/usr/bin/env bash
# Token Reduction Protocol Verification Harness
#
# Runs identical prompts with and without the token reduction protocol,
# captures token usage data, and produces a comparison report.
#
# Usage:
#   bash tests/token-verification/run-verification.sh
#
# Environment variables:
#   REPEAT_COUNT       Number of runs per prompt per mode (default: 3)
#   MODEL              Claude model to use (default: sonnet)
#   PROMPTS_FILE       Path to prompts JSON file (default: auto-detected)
#   SKILL_FILE         Path to token protocol skill file (default: auto-detected)
#   SKIP_QUALITY_CHECK Skip acceptance criteria validation (default: false)

set -euo pipefail

# --- Configuration ---

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

REPEAT_COUNT="${REPEAT_COUNT:-3}"
MODEL="${MODEL:-sonnet}"
PROMPTS_FILE="${PROMPTS_FILE:-$SCRIPT_DIR/prompts.json}"
SKILL_FILE="${SKILL_FILE:-$PROJECT_ROOT/.agents/TOKEN_PROTOCOL.md}"
SKIP_QUALITY_CHECK="${SKIP_QUALITY_CHECK:-false}"

TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
RESULTS_DIR="$SCRIPT_DIR/results/run-$TIMESTAMP"

# --- Preflight checks ---

check_dependencies() {
    local missing=0
    for cmd in claude jq; do
        if ! command -v "$cmd" &>/dev/null; then
            echo "ERROR: Required command '$cmd' not found." >&2
            missing=1
        fi
    done
    if [[ "$missing" -eq 1 ]]; then
        exit 1
    fi
}

check_files() {
    if [[ ! -f "$PROMPTS_FILE" ]]; then
        echo "ERROR: Prompts file not found: $PROMPTS_FILE" >&2
        exit 1
    fi
    if [[ ! -f "$SKILL_FILE" ]]; then
        echo "ERROR: Skill file not found: $SKILL_FILE" >&2
        exit 1
    fi
}

# --- Core functions ---

run_prompt() {
    local mode="$1"    # "baseline" or "protocol"
    local prompt="$2"
    local output_file="$3"

    local cli_args=( -p --output-format json --model "$MODEL" --bare --tools "" --no-session-persistence )

    if [[ "$mode" == "protocol" ]]; then
        cli_args+=( --append-system-prompt-file "$SKILL_FILE" )
    fi

    # SEC-001 mitigation: pass prompt via stdin, not shell interpolation
    # AUD-001 mitigation: capture stderr to log file instead of suppressing
    printf '%s' "$prompt" | claude "${cli_args[@]}" > "$output_file" 2>"${output_file}.stderr"

    return $?
}

extract_usage() {
    local json_file="$1"
    jq '{
        input_tokens: .usage.input_tokens,
        cache_creation_input_tokens: (.usage.cache_creation_input_tokens // 0),
        cache_read_input_tokens: (.usage.cache_read_input_tokens // 0),
        output_tokens: .usage.output_tokens,
        total_cost_usd: .total_cost_usd,
        duration_ms: .duration_ms,
        duration_api_ms: .duration_api_ms
    }' "$json_file"
}

evaluate_criteria() {
    local response_file="$1"
    local prompt_index="$2"

    local response_text
    response_text=$(jq -r '.result // ""' "$response_file")
    if [[ -z "$response_text" ]]; then
        echo '{"quality_pass": false, "passed": 0, "failed": 0, "failed_criteria": ["empty response"]}'; return
    fi

    local criteria_count
    criteria_count=$(jq ".prompts[$prompt_index].acceptance_criteria // [] | length" "$PROMPTS_FILE")
    if [[ "$criteria_count" -eq 0 ]]; then
        echo '{"quality_pass": true, "passed": 0, "failed": 0, "failed_criteria": [], "skipped": true}'; return
    fi

    local passed=0 failed=0 failed_criteria="[]"
    for c in $(seq 0 $((criteria_count - 1))); do
        local ctype cvalue clabel
        ctype=$(jq -r ".prompts[$prompt_index].acceptance_criteria[$c].type" "$PROMPTS_FILE")
        cvalue=$(jq -r ".prompts[$prompt_index].acceptance_criteria[$c].value" "$PROMPTS_FILE")
        clabel=$(jq -r ".prompts[$prompt_index].acceptance_criteria[$c].label" "$PROMPTS_FILE")
        local matched=false
        case "$ctype" in
            contains)     printf '%s' "$response_text" | grep -qiF -- "$cvalue" && matched=true || true ;;
            not_contains) printf '%s' "$response_text" | grep -qiF -- "$cvalue" || matched=true ;;
            regex)        printf '%s' "$response_text" | grep -qiE -- "$cvalue" && matched=true || true ;;
        esac
        if [[ "$matched" == "true" ]]; then
            passed=$((passed + 1))
        else
            failed=$((failed + 1))
            failed_criteria=$(echo "$failed_criteria" | jq --arg label "$clabel" '. + [$label]')
        fi
    done

    local quality_pass="true"
    [[ "$failed" -gt 0 ]] && quality_pass="false"
    jq -n --argjson passed "$passed" --argjson failed "$failed" \
        --argjson quality_pass "$quality_pass" --argjson failed_criteria "$failed_criteria" \
        '{quality_pass: $quality_pass, passed: $passed, failed: $failed, failed_criteria: $failed_criteria}'
}

# --- Main execution ---

main() {
    check_dependencies
    check_files

    local prompt_count
    prompt_count=$(jq '.prompts | length' "$PROMPTS_FILE")

    local quality_label
    if [[ "$SKIP_QUALITY_CHECK" == "true" ]]; then
        quality_label="DISABLED"
    else
        quality_label="ENABLED"
    fi

    echo "========================================"
    echo "Token Reduction Verification Harness"
    echo "========================================"
    echo "Date:           $(date -Iseconds)"
    echo "Model:          $MODEL"
    echo "Prompts:        $prompt_count"
    echo "Repetitions:    $REPEAT_COUNT per prompt per mode"
    echo "Total API calls: $((prompt_count * REPEAT_COUNT * 2))"
    echo "Results dir:    $RESULTS_DIR"
    echo "Skill file:     $SKILL_FILE"
    echo "Quality check:  $quality_label"
    echo "========================================"
    echo ""

    mkdir -p "$RESULTS_DIR/baseline" "$RESULTS_DIR/protocol"

    jq -n \
        --arg date "$(date -Iseconds)" \
        --arg model "$MODEL" \
        --arg repeat_count "$REPEAT_COUNT" \
        --arg skill_file "$SKILL_FILE" \
        --arg prompts_file "$PROMPTS_FILE" \
        --arg claude_version "$(claude --version 2>/dev/null || echo 'unknown')" \
        --arg skip_quality_check "$SKIP_QUALITY_CHECK" \
        '{
            date: $date,
            model: $model,
            repeat_count: ($repeat_count | tonumber),
            skill_file: $skill_file,
            prompts_file: $prompts_file,
            claude_version: $claude_version,
            skip_quality_check: ($skip_quality_check == "true")
        }' > "$RESULTS_DIR/metadata.json"

    local all_results="[]"

    for i in $(seq 0 $((prompt_count - 1))); do
        local prompt_id prompt_text prompt_category prompt_input_length
        prompt_id=$(jq -r ".prompts[$i].id" "$PROMPTS_FILE")
        prompt_text=$(jq -r ".prompts[$i].prompt" "$PROMPTS_FILE")
        prompt_category=$(jq -r ".prompts[$i].category" "$PROMPTS_FILE")
        prompt_input_length=$(jq -r ".prompts[$i].input_length" "$PROMPTS_FILE")

        echo "--- Prompt $((i + 1))/$prompt_count: $prompt_id ($prompt_category, $prompt_input_length) ---"

        local baseline_input_tokens="[]"
        local baseline_output_tokens="[]"
        local baseline_costs="[]"
        local baseline_durations="[]"
        local protocol_input_tokens="[]"
        local protocol_output_tokens="[]"
        local protocol_costs="[]"
        local protocol_durations="[]"
        local quality_results="[]"
        local all_quality_pass="true"

        for r in $(seq 1 "$REPEAT_COUNT"); do
            echo "  Run $r/$REPEAT_COUNT..."

            # Baseline run
            local baseline_file="$RESULTS_DIR/baseline/${prompt_id}-run${r}.json"
            echo -n "    Baseline: "
            if run_prompt "baseline" "$prompt_text" "$baseline_file"; then
                local b_usage
                b_usage=$(extract_usage "$baseline_file")
                local b_in b_out b_cost b_dur
                b_in=$(echo "$b_usage" | jq '.input_tokens')
                b_out=$(echo "$b_usage" | jq '.output_tokens')
                b_cost=$(echo "$b_usage" | jq '.total_cost_usd')
                b_dur=$(echo "$b_usage" | jq '.duration_api_ms')
                echo "${b_in} in / ${b_out} out / \$${b_cost}"
                baseline_input_tokens=$(echo "$baseline_input_tokens" | jq ". + [$b_in]")
                baseline_output_tokens=$(echo "$baseline_output_tokens" | jq ". + [$b_out]")
                baseline_costs=$(echo "$baseline_costs" | jq ". + [$b_cost]")
                baseline_durations=$(echo "$baseline_durations" | jq ". + [$b_dur]")
            else
                echo "FAILED"
            fi

            # Protocol run
            local protocol_file="$RESULTS_DIR/protocol/${prompt_id}-run${r}.json"
            echo -n "    Protocol: "
            if run_prompt "protocol" "$prompt_text" "$protocol_file"; then
                local p_usage
                p_usage=$(extract_usage "$protocol_file")
                local p_in p_out p_cost p_dur
                p_in=$(echo "$p_usage" | jq '.input_tokens')
                p_out=$(echo "$p_usage" | jq '.output_tokens')
                p_cost=$(echo "$p_usage" | jq '.total_cost_usd')
                p_dur=$(echo "$p_usage" | jq '.duration_api_ms')
                echo "${p_in} in / ${p_out} out / \$${p_cost}"
                protocol_input_tokens=$(echo "$protocol_input_tokens" | jq ". + [$p_in]")
                protocol_output_tokens=$(echo "$protocol_output_tokens" | jq ". + [$p_out]")
                protocol_costs=$(echo "$protocol_costs" | jq ". + [$p_cost]")
                protocol_durations=$(echo "$protocol_durations" | jq ". + [$p_dur]")

                if [[ "$SKIP_QUALITY_CHECK" != "true" ]]; then
                    local q_result
                    q_result=$(evaluate_criteria "$protocol_file" "$i")
                    quality_results=$(echo "$quality_results" | jq ". + [$q_result]")
                    local run_pass
                    run_pass=$(echo "$q_result" | jq -r '.quality_pass')
                    if [[ "$run_pass" != "true" ]]; then
                        all_quality_pass="false"
                        echo "    Quality: FAIL — $(echo "$q_result" | jq -r '.failed_criteria | join(", ")')"
                    else
                        local q_skipped
                        q_skipped=$(echo "$q_result" | jq -r '.skipped // false')
                        if [[ "$q_skipped" == "true" ]]; then
                            echo "    Quality: SKIP (no criteria defined)"
                        else
                            echo "    Quality: PASS ($(echo "$q_result" | jq -r '.passed') criteria)"
                        fi
                    fi
                fi
            else
                echo "FAILED"
            fi
        done

        # Compute per-prompt statistics (sign convention: baseline - protocol; positive = reduction)
        local prompt_result
        prompt_result=$(jq -n \
            --arg id "$prompt_id" \
            --arg category "$prompt_category" \
            --arg input_length "$prompt_input_length" \
            --argjson b_in "$baseline_input_tokens" \
            --argjson b_out "$baseline_output_tokens" \
            --argjson b_cost "$baseline_costs" \
            --argjson b_dur "$baseline_durations" \
            --argjson p_in "$protocol_input_tokens" \
            --argjson p_out "$protocol_output_tokens" \
            --argjson p_cost "$protocol_costs" \
            --argjson p_dur "$protocol_durations" \
            --argjson quality_pass "$all_quality_pass" \
            --argjson quality_results "$quality_results" \
            --arg skip_quality "$SKIP_QUALITY_CHECK" \
            '{
                id: $id,
                category: $category,
                input_length: $input_length,
                baseline: {
                    input_tokens:  { values: $b_in,  mean: ($b_in  | add / length), min: ($b_in  | min), max: ($b_in  | max) },
                    output_tokens: { values: $b_out, mean: ($b_out | add / length), min: ($b_out | min), max: ($b_out | max) },
                    cost_usd:      { values: $b_cost, mean: ($b_cost | add / length) },
                    duration_ms:   { values: $b_dur, mean: ($b_dur | add / length) }
                },
                protocol: {
                    input_tokens:  { values: $p_in,  mean: ($p_in  | add / length), min: ($p_in  | min), max: ($p_in  | max) },
                    output_tokens: { values: $p_out, mean: ($p_out | add / length), min: ($p_out | min), max: ($p_out | max) },
                    cost_usd:      { values: $p_cost, mean: ($p_cost | add / length) },
                    duration_ms:   { values: $p_dur, mean: ($p_dur | add / length) }
                },
                quality: {
                    pass: $quality_pass,
                    skipped: ($skip_quality == "true"),
                    results: $quality_results
                },
                delta: {
                    output_tokens_pct: (if ($b_out | add / length) > 0 then ((($b_out | add / length) - ($p_out | add / length)) / ($b_out | add / length) * 100) else 0 end),
                    cost_pct: (if ($b_cost | add / length) > 0 then ((($b_cost | add / length) - ($p_cost | add / length)) / ($b_cost | add / length) * 100) else 0 end),
                    valid: $quality_pass
                }
            }')

        all_results=$(echo "$all_results" | jq ". + [$prompt_result]")
        echo ""
    done

    # Compute aggregate statistics
    local summary
    summary=$(echo "$all_results" | jq '{
        prompts: .,
        aggregate: {
            total_baseline_output_mean: [.[].baseline.output_tokens.mean] | add,
            total_protocol_output_mean: [.[].protocol.output_tokens.mean] | add,
            total_baseline_cost_mean: [.[].baseline.cost_usd.mean] | add,
            total_protocol_cost_mean: [.[].protocol.cost_usd.mean] | add,
            output_token_reduction_pct: (
                if ([.[].baseline.output_tokens.mean] | add) > 0
                then ((([.[].baseline.output_tokens.mean] | add) - ([.[].protocol.output_tokens.mean] | add)) / ([.[].baseline.output_tokens.mean] | add) * 100)
                else 0 end
            ),
            cost_reduction_pct: (
                if ([.[].baseline.cost_usd.mean] | add) > 0
                then ((([.[].baseline.cost_usd.mean] | add) - ([.[].protocol.cost_usd.mean] | add)) / ([.[].baseline.cost_usd.mean] | add) * 100)
                else 0 end
            )
        },
        quality_validated: {
            prompt_count: [.[] | select(.quality.pass == true and .quality.skipped == false)] | length,
            output_token_reduction_pct: (
                if ([.[] | select(.quality.pass == true and .quality.skipped == false) | .baseline.output_tokens.mean] | add // 0) > 0
                then ((([.[] | select(.quality.pass == true and .quality.skipped == false) | .baseline.output_tokens.mean] | add) - ([.[] | select(.quality.pass == true and .quality.skipped == false) | .protocol.output_tokens.mean] | add)) / ([.[] | select(.quality.pass == true and .quality.skipped == false) | .baseline.output_tokens.mean] | add) * 100)
                else 0 end
            ),
            cost_reduction_pct: (
                if ([.[] | select(.quality.pass == true and .quality.skipped == false) | .baseline.cost_usd.mean] | add // 0) > 0
                then ((([.[] | select(.quality.pass == true and .quality.skipped == false) | .baseline.cost_usd.mean] | add) - ([.[] | select(.quality.pass == true and .quality.skipped == false) | .protocol.cost_usd.mean] | add)) / ([.[] | select(.quality.pass == true and .quality.skipped == false) | .baseline.cost_usd.mean] | add) * 100)
                else 0 end
            ),
            failed_prompts: [.[] | select(.quality.pass == false) | .id]
        },
        by_input_length: (
            group_by(.input_length) | map({
                input_length: .[0].input_length,
                prompt_count: length,
                baseline_output_mean: ([.[].baseline.output_tokens.mean] | add),
                protocol_output_mean: ([.[].protocol.output_tokens.mean] | add),
                output_token_reduction_pct: (
                    if ([.[].baseline.output_tokens.mean] | add) > 0
                    then ((([.[].baseline.output_tokens.mean] | add) - ([.[].protocol.output_tokens.mean] | add)) / ([.[].baseline.output_tokens.mean] | add) * 100)
                    else 0 end
                )
            })
        )
    }')

    echo "$summary" > "$RESULTS_DIR/summary.json"

    generate_report "$summary" > "$RESULTS_DIR/report.md"

    echo "========================================"
    echo "RESULTS SUMMARY"
    echo "========================================"
    echo ""
    echo "$summary" | jq -r '
        "Aggregate Results:",
        "  Baseline output tokens (mean total): \(.aggregate.total_baseline_output_mean)",
        "  Protocol output tokens (mean total): \(.aggregate.total_protocol_output_mean)",
        "  Output token reduction: \(.aggregate.output_token_reduction_pct | . * 100 | round / 100)%",
        "",
        "  Baseline cost (mean total): $\(.aggregate.total_baseline_cost_mean | . * 10000 | round / 10000)",
        "  Protocol cost (mean total): $\(.aggregate.total_protocol_cost_mean | . * 10000 | round / 10000)",
        "  Cost reduction: \(.aggregate.cost_reduction_pct | . * 100 | round / 100)%",
        "",
        "Quality-Validated Results (\(.quality_validated.prompt_count) prompts passed):",
        "  Output token reduction: \(.quality_validated.output_token_reduction_pct | . * 100 | round / 100)%",
        "  Cost reduction: \(.quality_validated.cost_reduction_pct | . * 100 | round / 100)%",
        (if (.quality_validated.failed_prompts | length) > 0 then "  Failed: \(.quality_validated.failed_prompts | join(", "))" else empty end),
        "",
        "By Input Length:",
        (.by_input_length[] | "  \(.input_length) (\(.prompt_count) prompts): \(.output_token_reduction_pct | . * 100 | round / 100)% reduction"),
        "",
        "Per-Prompt Breakdown:",
        (.prompts[] | "  \(.id) (\(.category), \(.input_length)): \(.delta.output_tokens_pct | . * 100 | round / 100)% reduction\(if .quality.skipped then "" elif .delta.valid then " [PASS]" else " [FAIL]" end)")
    '
    echo ""
    echo "Full results: $RESULTS_DIR/"
    echo "Summary JSON: $RESULTS_DIR/summary.json"
    echo "Report:       $RESULTS_DIR/report.md"
}

generate_report() {
    local summary="$1"

    echo "# Token Reduction Verification Report"
    echo ""
    echo "Date: $(date -Iseconds)"
    echo "Model: $MODEL"
    echo "Repetitions per prompt: $REPEAT_COUNT"
    echo "Quality check: $(if [[ "$SKIP_QUALITY_CHECK" == "true" ]]; then echo "DISABLED"; else echo "ENABLED"; fi)"
    echo ""
    echo "## Aggregate Results"
    echo ""
    echo "| Metric | Baseline (mean) | Protocol (mean) | Reduction |"
    echo "|--------|-----------------|-----------------|-----------|"

    echo "$summary" | jq -r '
        "| Output tokens | \(.aggregate.total_baseline_output_mean) | \(.aggregate.total_protocol_output_mean) | \(.aggregate.output_token_reduction_pct | . * 100 | round / 100)% |",
        "| Cost (USD) | $\(.aggregate.total_baseline_cost_mean | . * 10000 | round / 10000) | $\(.aggregate.total_protocol_cost_mean | . * 10000 | round / 10000) | \(.aggregate.cost_reduction_pct | . * 100 | round / 100)% |"
    '

    echo ""
    echo "### Quality-Validated Results"
    echo ""
    echo "$summary" | jq -r '
        "Prompts passing quality check: \(.quality_validated.prompt_count) of \(.prompts | length)",
        "",
        "| Metric | Reduction (quality-validated only) |",
        "|--------|------------------------------------|",
        "| Output tokens | \(.quality_validated.output_token_reduction_pct | . * 100 | round / 100)% |",
        "| Cost (USD) | \(.quality_validated.cost_reduction_pct | . * 100 | round / 100)% |"
    '

    if echo "$summary" | jq -e '.quality_validated.failed_prompts | length > 0' >/dev/null 2>&1; then
        echo ""
        echo "**Quality failures:** $(echo "$summary" | jq -r '.quality_validated.failed_prompts | join(", ")')"
    fi

    echo ""
    echo "## Results by Input Length"
    echo ""
    echo "| Input Length | Prompts | Baseline Out (mean total) | Protocol Out (mean total) | Reduction |"
    echo "|-------------|---------|---------------------------|---------------------------|-----------|"

    echo "$summary" | jq -r '
        .by_input_length[] |
        "| \(.input_length) | \(.prompt_count) | \(.baseline_output_mean) | \(.protocol_output_mean) | \(.output_token_reduction_pct | . * 100 | round / 100)% |"
    '

    echo ""
    echo "## Per-Prompt Results"
    echo ""
    echo "| Prompt | Category | Input Length | Baseline Out (mean) | Protocol Out (mean) | Reduction | Quality |"
    echo "|--------|----------|-------------|---------------------|---------------------|-----------|---------|"

    echo "$summary" | jq -r '
        .prompts[] |
        "| \(.id) | \(.category) | \(.input_length) | \(.baseline.output_tokens.mean) | \(.protocol.output_tokens.mean) | \(.delta.output_tokens_pct | . * 100 | round / 100)% | \(if .quality.skipped then "SKIP" elif .quality.pass then "PASS" else "FAIL" end) |"
    '

    echo ""
    echo "## Methodology"
    echo ""
    echo "Each prompt was run $REPEAT_COUNT times in each mode (baseline and protocol)."
    echo "Baseline: \`claude -p --bare --tools \"\" --model $MODEL\`"
    echo "Protocol: \`claude -p --bare --tools \"\" --model $MODEL --append-system-prompt-file SKILL.md\`"
    echo ""
    echo "**Sign convention:** All percentage metrics use (baseline minus protocol) divided"
    echo "by baseline. Positive values indicate the protocol reduced usage (the desired"
    echo "outcome). Negative values indicate the protocol increased usage. This convention"
    echo "applies uniformly across aggregate, by-input-length, and per-prompt tables."
    echo ""
    echo "**Quality gating:** Each protocol response is evaluated against per-prompt"
    echo "acceptance criteria defined in prompts.json. Token and cost reductions are"
    echo "reported for all prompts but are only considered validated when the quality"
    echo "check passes. The Quality-Validated Results section excludes prompts that"
    echo "failed acceptance criteria. Use SKIP_QUALITY_CHECK=true to disable."
    echo ""
    echo "## Raw Data"
    echo ""
    echo "Raw API responses are preserved in the \`baseline/\` and \`protocol/\` subdirectories"
    echo "of this run's results folder for inspection and reanalysis."
}

main "$@"
