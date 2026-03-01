$ErrorActionPreference = "Continue"

git fetch origin master

git checkout -B feature/spec-registry-infrastructure origin/master
git checkout feature/automated-spec-clarification -- .agent .clinerules .gitignore .specify GEMINI.md
git reset HEAD .agent/scripts/clarify_spec.py
git checkout -- .agent/scripts/clarify_spec.py
Remove-Item -Path .agent/scripts/clarify_spec.py -ErrorAction Ignore
git add .
$infraStatus = git status --porcelain
if ($infraStatus) {
    git commit -m "docs: add base spec templates and agent workflows"
    git push origin feature/spec-registry-infrastructure --force
    # Try creating PR, ignore error if already exists
    gh pr create --title "docs: spec registry infrastructure" --body "Automated PR adding base spec configuration." --base master
}

$specDirs = @(
    "001-ocr-parser", "002-dice-core", "003-dice-evaluator", "004-dice-parser",
    "005-rag-pipeline", "006-rules-validation-parser", "007-battle-transcript-engine",
    "008-entropy-buffer-service", "009-cross-domain-agents", "010-agent-persistence-layer",
    "011-agent-security-isolation", "012-system-audit-log", "013-logi-slate-ui-framework",
    "014-economy-management-engine", "015-warscribe-core-notation", "016-oracle-intelligence-suite",
    "017-platform-evolution-map", "018-modular-ecosystem-registry", "019-real-time-tournament-pairing",
    "020-live-stream-overlay-widget", "021-team-club-management", "022-voice-to-text-battle-logging",
    "023-mobile-companion-app", "024-hardware-dice-tower-integration", "025-ar-table-overlay",
    "026-voice-activated-scorekeeping", "027-visual-army-painter", "028-coaching-marketplace",
    "029-to-dashboard", "030-anti-cheat-analysis", "031-cross-game-inventory-sync",
    "032-campaign-map-engine", "033-subscription-gifting", "034-battle-replay-heatmaps",
    "035-local-store-locator", "036-twitch-extension-integration", "037-smart-watch-score-counter",
    "038-archetype-id", "039-faq-scraper", "040-reputation-system", "041-data-export",
    "042-i18n-support", "043-offline-mode", "045-positional-heuristics",
    "046-roster-synergy", "047-upset-detector"
)

foreach ($spec in $specDirs) {
    Write-Host "Processing $spec ..."
    $branchName = "feat/spec-$spec"
    git checkout -B $branchName origin/master
    git checkout feature/automated-spec-clarification -- "$spec"
    git add "$spec"
    $status = git status --porcelain
    if ($status) {
        git commit -m "docs: add specification for $spec"
        git push origin $branchName -u --force
        gh pr create --title "docs: specification for $spec" --body "Extracted specification and checklists for feature **$spec**." --base master
    } else {
        Write-Host "No changes for $spec, skipping."
    }
}

git checkout master
