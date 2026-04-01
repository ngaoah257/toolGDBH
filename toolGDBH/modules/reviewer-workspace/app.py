from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict
from pathlib import Path

import dearpygui.dearpygui as dpg

APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parents[1]
EXTRA_PATHS = [
    PROJECT_ROOT / "shared" / "types",
    PROJECT_ROOT / "shared",
    PROJECT_ROOT / "modules" / "parser-normalizer" / "src",
    PROJECT_ROOT / "modules" / "eligibility-service" / "src",
    PROJECT_ROOT / "modules" / "master-data-service" / "src",
    PROJECT_ROOT / "modules" / "deterministic-rule-engine" / "src",
    PROJECT_ROOT / "modules" / "diagnosis-validator" / "src",
    PROJECT_ROOT / "modules" / "evidence-service" / "src",
    PROJECT_ROOT / "modules" / "reviewer-workspace" / "src",
    PROJECT_ROOT / "modules" / "rule-registry" / "src",
    PROJECT_ROOT / "modules" / "case-triage" / "src",
]

for extra_path in EXTRA_PATHS:
    extra = str(extra_path)
    if extra not in sys.path:
        sys.path.insert(0, extra)

from reviewer_workspace import (
    ClinicalPolicyRecord,
    PaymentPolicyRecord,
    PreviewRunResult,
    ReviewerWorkspaceService,
    RuleEditorRecord,
    XML5RetrievalPreviewResult,
)


def resolve_existing_path(candidates: list[Path]) -> Path | None:
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def resolve_path_from_env(env_name: str, fallback_candidates: list[Path]) -> Path | None:
    raw_value = os.getenv(env_name, "").strip()
    if raw_value:
        return Path(raw_value)
    return resolve_existing_path(fallback_candidates)


RULE_FILE = PROJECT_ROOT / "modules" / "rule-registry" / "config" / "rules.mwp.json"
CATALOG_DIR = resolve_path_from_env(
    "TOOLGDBH_CATALOG_DIR",
    [PROJECT_ROOT / "Danhmuc", PROJECT_ROOT.parent / "Danhmuc"],
)
ELIGIBILITY_POLICY_FILE = resolve_path_from_env(
    "TOOLGDBH_ELIGIBILITY_POLICY_FILE",
    [PROJECT_ROOT / "modules" / "eligibility-service" / "config" / "policy.mwp.json"],
)
PAYMENT_POLICY_FILE = resolve_path_from_env(
    "TOOLGDBH_PAYMENT_POLICY_FILE",
    [PROJECT_ROOT / "modules" / "deterministic-rule-engine" / "config" / "payment_policy.mwp.json"],
)
CLINICAL_POLICY_FILE = resolve_path_from_env(
    "TOOLGDBH_CLINICAL_POLICY_FILE",
    [PROJECT_ROOT / "modules" / "deterministic-rule-engine" / "config" / "clinical_policy.mwp.json"],
)
DEFAULT_XML_FILE = resolve_path_from_env(
    "TOOLGDBH_DEFAULT_XML_FILE",
    [
        PROJECT_ROOT / "xulyXML" / "XML" / "data_112645_HT3382796012783_25029071_3176.xml",
        PROJECT_ROOT.parent / "xulyXML" / "XML" / "data_112645_HT3382796012783_25029071_3176.xml",
    ],
)
KB_CHUNKS_FILE = resolve_path_from_env(
    "TOOLGDBH_KB_CHUNKS_FILE",
    [PROJECT_ROOT / "runtime" / "knowledge-base" / "chunks" / "xml5_note_records.chunks.jsonl"],
)
GUIDELINE_RULE_DRAFTS_FILE = resolve_path_from_env(
    "TOOLGDBH_GUIDELINE_RULE_DRAFTS_FILE",
    [PROJECT_ROOT / "runtime" / "guideline-rules" / "drafts" / "guideline_rule_drafts.jsonl"],
)
INTERNAL_CODE_POLICY_FILE = resolve_path_from_env(
    "TOOLGDBH_INTERNAL_CODE_POLICY_FILE",
    [PROJECT_ROOT / "modules" / "deterministic-rule-engine" / "config" / "internal_code_policy.mwp.json"],
)
DIAGNOSIS_PROFILES_FILE = resolve_path_from_env(
    "TOOLGDBH_DIAGNOSIS_PROFILES_FILE",
    [PROJECT_ROOT / "runtime" / "diagnosis-validation" / "profiles" / "sample_diagnosis_profiles.jsonl"],
)

SEVERITY_LABELS = {
    "info": "Thông tin",
    "warning": "Cảnh báo",
    "pending": "Chờ bổ sung",
    "reject": "Từ chối",
}
INPUT_SCOPE_LABELS = {
    "claim": "Toàn hồ sơ",
    "line": "Từng dòng chi phí",
}
SUGGESTED_ACTION_LABELS = {
    "warn": "Cảnh báo",
    "request_more": "Yêu cầu bổ sung hồ sơ",
    "reduce": "Giảm trừ chi phí",
    "reject": "Từ chối thanh toán",
    "accept": "Chấp nhận",
}
SEVERITY_KEYS_BY_LABEL = {label: key for key, label in SEVERITY_LABELS.items()}
INPUT_SCOPE_KEYS_BY_LABEL = {label: key for key, label in INPUT_SCOPE_LABELS.items()}
SUGGESTED_ACTION_KEYS_BY_LABEL = {label: key for key, label in SUGGESTED_ACTION_LABELS.items()}

PREVIEW_GROUP_ORDER = ["GUIDELINE", "PAY", "MASTER", "LOGIC", "ELIG", "OTHER"]
PREVIEW_GROUP_TITLES = {
    "GUIDELINE": "GL.* - Guideline Draft",
    "PAY": "PAY.* - Thanh toán",
    "MASTER": "MASTER.* - Danh mục và nhân lực",
    "LOGIC": "LOGIC.* - Nghiệp vụ và lâm sàng",
    "ELIG": "ELIG.* - Điều kiện BHYT",
    "OTHER": "Khác",
}
PREVIEW_GROUP_ALL = "ALL"
SEVERITY_SORT_ORDER = {
    "reject": 0,
    "pending": 1,
    "warning": 2,
    "info": 3,
}
BADGE_THEME_TAGS = {
    "selected": "theme_badge_selected",
    "reject": "theme_badge_reject",
    "pending": "theme_badge_pending",
    "warning": "theme_badge_warning",
    "info": "theme_badge_info",
    "default": "theme_badge_default",
}

TAG_STATUS = "status_text"
TAG_SEARCH = "search_field"
TAG_RULE_LIST = "rule_list_container"
TAG_RULE_ID = "rule_id_field"
TAG_RULE_NAME = "rule_name_field"
TAG_RULE_GROUP = "rule_group_field"
TAG_SEVERITY = "severity_combo"
TAG_INPUT_SCOPE = "input_scope_combo"
TAG_SUGGESTED_ACTION = "suggested_action_combo"
TAG_LEGAL_BASIS = "legal_basis_field"
TAG_OWNER = "owner_field"
TAG_EFFECTIVE_FROM = "effective_from_field"
TAG_EFFECTIVE_TO = "effective_to_field"
TAG_ENABLED = "enabled_checkbox"
TAG_DECISION_LOGIC = "decision_logic_field"
TAG_PAYMENT_SOURCE = "payment_source_field"
TAG_PAYMENT_SERVICE_CODES = "payment_service_codes_field"
TAG_PAYMENT_DRUG_CODES = "payment_drug_codes_field"
TAG_PAYMENT_SUPPLY_CODES = "payment_supply_codes_field"
TAG_PAYMENT_SERVICE_KEYWORDS = "payment_service_keywords_field"
TAG_PAYMENT_DRUG_KEYWORDS = "payment_drug_keywords_field"
TAG_PAYMENT_SUPPLY_KEYWORDS = "payment_supply_keywords_field"
TAG_CLINICAL_SOURCE = "clinical_source_field"
TAG_CLINICAL_JSON = "clinical_json_field"
TAG_PREVIEW_XML = "preview_xml_field"
TAG_PREVIEW_DATE = "preview_date_field"
TAG_PREVIEW_EXPORT = "preview_export_field"
TAG_PREVIEW_SUMMARY = "preview_summary_text"
TAG_PREVIEW_GROUPS = "preview_group_container"
TAG_PREVIEW_HITS = "preview_hits_container"
TAG_XML5_RETRIEVAL_EXPORT = "xml5_retrieval_export_field"
TAG_XML5_RETRIEVAL_SUMMARY = "xml5_retrieval_summary_text"
TAG_XML5_RETRIEVAL_CONTAINER = "xml5_retrieval_container"
TAG_DIAGNOSIS_SUMMARY = "diagnosis_summary_text"
TAG_DIAGNOSIS_CONTAINER = "diagnosis_container"
TAG_SETUP_CONTAINER = "setup_container"
TAG_FILE_DIALOG = "xml_file_dialog"


def display_value(value: str, label_map: dict[str, str]) -> str:
    return label_map.get(value, value)


def parse_list_field(raw_value: str) -> list[str]:
    normalized = raw_value.replace("\n", ",")
    return [item.strip() for item in normalized.split(",") if item.strip()]


def join_list_field(values: list[str]) -> str:
    return ", ".join(values)


def preview_group_key(rule_id: str) -> str:
    prefix = (rule_id or "").split(".", 1)[0].upper()
    if prefix in {"PAY", "MASTER", "LOGIC", "ELIG"}:
        return prefix
    if prefix in {"GL", "GUIDELINE"}:
        return "GUIDELINE"
    return "OTHER"


def format_amount(value: object) -> str:
    try:
        numeric = float(value or 0)
    except (TypeError, ValueError):
        numeric = 0.0
    return f"{numeric:,.0f}"


def severity_sort_key(severity: str) -> int:
    return SEVERITY_SORT_ORDER.get((severity or "").lower(), 99)


def highest_group_severity(hits: list[object]) -> str:
    if not hits:
        return "default"
    severities = [str(getattr(hit, "severity", "")).lower() for hit in hits]
    return min(severities, key=severity_sort_key)


def severity_color(severity: str) -> tuple[int, int, int]:
    normalized = (severity or "").lower()
    if normalized == "reject":
        return (185, 28, 28)
    if normalized == "pending":
        return (234, 88, 12)
    if normalized == "warning":
        return (202, 138, 4)
    return (37, 99, 235)


def severity_panel_title(severity: str) -> str:
    normalized = (severity or "").lower()
    if normalized == "reject":
        return "LOI CAN XU LY"
    if normalized == "pending":
        return "THIEU CHUNG CU"
    if normalized == "warning":
        return "CANH BAO CAN XEM LAI"
    return "THONG TIN DOI CHIEU"


def hit_problem_label(hit: object) -> str:
    rule_group = preview_group_key(str(getattr(hit, "rule_id", "")))
    severity = str(getattr(hit, "severity", "")).lower()
    if rule_group == "GUIDELINE":
        return "Thiếu chứng cứ theo guideline draft"
    if severity == "reject":
        return "Lỗi nghiêm trọng hoặc ngoài phạm vi thanh toán"
    if severity == "pending":
        return "Thiếu chứng từ hoặc cần bổ sung căn cứ"
    if severity == "warning":
        return "Bất thường nghiệp vụ cần rà soát"
    return "Thông tin đối chiếu"


def diagnosis_status_color(status: str) -> tuple[int, int, int]:
    normalized = (status or "").lower()
    if normalized == "strong_match":
        return (22, 163, 74)
    if normalized == "partial_match":
        return (202, 138, 4)
    if normalized in {"missing_evidence", "missing_profile"}:
        return (234, 88, 12)
    if normalized == "suspected_mismatch":
        return (185, 28, 28)
    return (37, 99, 235)


def ensure_runtime_path(path_value: str) -> Path:
    path = Path(path_value)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def resolve_ui_font() -> Path | None:
    candidates = [
        Path(r"C:\Windows\Fonts\segoeui.ttf"),
        Path(r"C:\Windows\Fonts\tahoma.ttf"),
        Path(r"C:\Windows\Fonts\arial.ttf"),
    ]
    return resolve_existing_path(candidates)


def configure_badge_theme(tag: str, button_color: tuple[int, int, int], text_color: tuple[int, int, int]) -> None:
    with dpg.theme(tag=tag):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, button_color)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, button_color)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, button_color)
            dpg.add_theme_color(dpg.mvThemeCol_Text, text_color)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 6)


def build_themes() -> None:
    configure_badge_theme(BADGE_THEME_TAGS["selected"], (45, 55, 72), (255, 255, 255))
    configure_badge_theme(BADGE_THEME_TAGS["reject"], (184, 28, 28), (255, 255, 255))
    configure_badge_theme(BADGE_THEME_TAGS["pending"], (234, 88, 12), (255, 255, 255))
    configure_badge_theme(BADGE_THEME_TAGS["warning"], (253, 224, 71), (17, 24, 39))
    configure_badge_theme(BADGE_THEME_TAGS["info"], (191, 219, 254), (17, 24, 39))
    configure_badge_theme(BADGE_THEME_TAGS["default"], (226, 232, 240), (30, 41, 59))


def build_fonts() -> None:
    font_path = resolve_ui_font()
    if font_path is None:
        return
    with dpg.font_registry():
        with dpg.font(str(font_path), 18, tag="font_ui_vi"):
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range(0x00C0, 0x024F)
            dpg.add_font_range(0x1E00, 0x1EFF)
    dpg.bind_font("font_ui_vi")


def badge_theme_for_group(group_key: str, selected_group: str, hits: list[object]) -> str:
    if selected_group == group_key:
        return BADGE_THEME_TAGS["selected"]
    return BADGE_THEME_TAGS.get(highest_group_severity(hits), BADGE_THEME_TAGS["default"])


def build_app() -> None:
    service = ReviewerWorkspaceService(
        RULE_FILE,
        CATALOG_DIR,
        ELIGIBILITY_POLICY_FILE,
        PAYMENT_POLICY_FILE,
        CLINICAL_POLICY_FILE,
        KB_CHUNKS_FILE,
        GUIDELINE_RULE_DRAFTS_FILE,
        INTERNAL_CODE_POLICY_FILE,
        DIAGNOSIS_PROFILES_FILE,
    )
    payment_policy = service.get_payment_policy()
    clinical_policy = service.get_clinical_policy()
    state: dict[str, object] = {
        "selected_rule_id": None,
        "selected_preview_group": PREVIEW_GROUP_ALL,
        "last_preview_result": None,
        "last_xml5_retrieval_result": None,
        "selected_xml5_note_id": None,
    }

    def current_rules() -> list[RuleEditorRecord]:
        return service.list_rules()

    def set_status(message: str, color: tuple[int, int, int] = (71, 85, 105)) -> None:
        dpg.set_value(TAG_STATUS, message)
        dpg.configure_item(TAG_STATUS, color=color)

    def get_value(tag: str) -> str:
        return str(dpg.get_value(tag) or "")

    def get_combo_key(tag: str, label_map: dict[str, str], reverse_map: dict[str, str]) -> str:
        raw_value = get_value(tag)
        return reverse_map.get(raw_value, raw_value)

    def set_combo_value(tag: str, value: str, label_map: dict[str, str]) -> None:
        dpg.set_value(tag, display_value(value, label_map))

    def clear_container(tag: str) -> None:
        dpg.delete_item(tag, children_only=True)

    def render_setup_overview() -> None:
        clear_container(TAG_SETUP_CONTAINER)

        def add_path_row(label: str, path: Path | None) -> None:
            status = "Có" if path is not None and path.exists() else "Thiếu"
            color = (22, 163, 74) if status == "Có" else (220, 38, 38)
            dpg.add_text(f"{label}: {path if path is not None else '-'}", parent=TAG_SETUP_CONTAINER, wrap=980)
            dpg.add_text(f"Trạng thái: {status}", parent=TAG_SETUP_CONTAINER, color=color)
            dpg.add_separator(parent=TAG_SETUP_CONTAINER)

        def add_count_card(title: str, count: int, detail: str) -> None:
            with dpg.child_window(parent=TAG_SETUP_CONTAINER, border=True, height=90, autosize_x=True):
                dpg.add_text(title, color=(30, 41, 59))
                dpg.add_text(f"Số lượng: {count}", color=(37, 99, 235))
                dpg.add_text(detail, wrap=930, color=(71, 85, 105))

        dpg.add_text("Nguồn dữ liệu giám định", parent=TAG_SETUP_CONTAINER, color=(30, 41, 59))
        add_path_row("Thư mục danh mục", CATALOG_DIR)
        add_path_row("File rule", RULE_FILE)
        add_path_row("Eligibility policy", ELIGIBILITY_POLICY_FILE)
        add_path_row("Payment policy", PAYMENT_POLICY_FILE)
        add_path_row("Clinical policy", CLINICAL_POLICY_FILE)
        add_path_row("Guideline drafts", GUIDELINE_RULE_DRAFTS_FILE)
        add_path_row("Internal code policy", INTERNAL_CODE_POLICY_FILE)
        add_path_row("Diagnosis profiles", DIAGNOSIS_PROFILES_FILE)
        add_path_row("KB chunks", KB_CHUNKS_FILE)

        if CATALOG_DIR is None or not CATALOG_DIR.exists():
            dpg.add_text(
                "Chưa có thư mục danh mục để nạp thông tin giám định.",
                parent=TAG_SETUP_CONTAINER,
                color=(220, 38, 38),
            )
            return

        try:
            snapshot = MasterDataService(CATALOG_DIR).load_snapshot("2026-03-30")
        except Exception as exc:
            dpg.add_text(
                f"Không thể nạp snapshot danh mục: {exc}",
                parent=TAG_SETUP_CONTAINER,
                color=(220, 38, 38),
                wrap=980,
            )
            return

        dpg.add_text(
            f"Dataset version: {snapshot.dataset_version}",
            parent=TAG_SETUP_CONTAINER,
            wrap=980,
            color=(71, 85, 105),
        )
        dpg.add_separator(parent=TAG_SETUP_CONTAINER)
        add_count_card(
            "Nhân lực",
            len(snapshot.staff_members),
            "Danh mục từ FileNhanVienYTe.xlsx, dùng để đối chiếu bác sĩ, khoa, phạm vi chuyên môn.",
        )
        add_count_card(
            "Trang thiết bị",
            len(snapshot.equipment_items),
            "Danh mục từ FileTrangThietBi.xlsx, dùng để đối chiếu MA_MAY và điều kiện thực hiện dịch vụ.",
        )
        add_count_card(
            "Thuốc",
            len(snapshot.drug_items),
            "Danh mục thuốc hiệu lực tại 2026-03-30, dùng cho đối chiếu đơn giá, nhóm BHYT và hiệu lực.",
        )
        add_count_card(
            "VTYT",
            len(snapshot.supply_items),
            "Danh mục vật tư y tế hiệu lực tại 2026-03-30, dùng cho đối chiếu nhóm và đơn giá.",
        )
        add_count_card(
            "Dịch vụ",
            len(snapshot.service_items),
            "Danh mục dịch vụ bệnh viện hiệu lực tại 2026-03-30, dùng cho giá, chuyển tuyến và CLS.",
        )

    def note_map_by_line_id() -> dict[str, list[object]]:
        latest = state["last_xml5_retrieval_result"]
        if latest is None:
            return {}
        mapped: dict[str, list[object]] = {}
        for note in latest.note_records:
            for line_id in note.linked_line_ids:
                mapped.setdefault(line_id, []).append(note)
        return mapped

    def selected_xml5_note() -> object | None:
        latest = state["last_xml5_retrieval_result"]
        selected_note_id = state["selected_xml5_note_id"]
        if latest is None or selected_note_id is None:
            return None
        for note in latest.note_records:
            if note.note_id == selected_note_id:
                return note
        return None

    def render_xml5_retrieval(result: XML5RetrievalPreviewResult | None) -> None:
        state["last_xml5_retrieval_result"] = result
        clear_container(TAG_XML5_RETRIEVAL_CONTAINER)
        if result is None:
            state["selected_xml5_note_id"] = None
            dpg.set_value(
                TAG_XML5_RETRIEVAL_SUMMARY,
                "Chưa chạy XML5 retrieval hoặc chưa có knowledge-base chunk.",
            )
            return

        retrieval_by_query_id = {item.query_id: item for item in result.retrieval_results}
        dpg.set_value(
            TAG_XML5_RETRIEVAL_SUMMARY,
            f"XML5 retrieval | {len(result.note_records)} note | "
            f"{sum(1 for item in result.retrieval_results if item.results)} note có top-k chunk",
        )
        if not result.note_records:
            dpg.add_text(
                "File XML này không có XML5 note để retrieval.",
                parent=TAG_XML5_RETRIEVAL_CONTAINER,
                color=(71, 85, 105),
            )
            return

        if state["selected_xml5_note_id"] and not any(
            note.note_id == state["selected_xml5_note_id"] for note in result.note_records
        ):
            state["selected_xml5_note_id"] = None

        def apply_xml5_note_filter(note_id: str | None) -> None:
            state["selected_xml5_note_id"] = note_id
            latest_preview = state["last_preview_result"]
            latest_retrieval = state["last_xml5_retrieval_result"]
            if latest_retrieval is not None:
                render_xml5_retrieval(latest_retrieval)
            if latest_preview is not None:
                render_preview(latest_preview)

        with dpg.group(parent=TAG_XML5_RETRIEVAL_CONTAINER, horizontal=True):
            all_button = dpg.add_button(
                label="ALL XML5 notes",
                callback=lambda s, a, u=None: apply_xml5_note_filter(None),
            )
            dpg.bind_item_theme(
                all_button,
                BADGE_THEME_TAGS["selected"]
                if not state["selected_xml5_note_id"]
                else BADGE_THEME_TAGS["default"],
            )

        for note in result.note_records:
            query_id = f"query:{note.claim_id}:{note.note_id}"
            retrieval = retrieval_by_query_id.get(query_id)
            with dpg.child_window(parent=TAG_XML5_RETRIEVAL_CONTAINER, border=True, height=210, autosize_x=True):
                with dpg.group(horizontal=True):
                    note_button = dpg.add_button(
                        label=f"{note.note_id} | {note.note_type}",
                        callback=lambda s, a, u=note.note_id: apply_xml5_note_filter(u),
                    )
                    dpg.bind_item_theme(
                        note_button,
                        BADGE_THEME_TAGS["selected"]
                        if state["selected_xml5_note_id"] == note.note_id
                        else BADGE_THEME_TAGS["default"],
                    )
                dpg.add_text(
                    f"Tags: {', '.join(note.context_tags) if note.context_tags else '-'}"
                )
                dpg.add_text(
                    f"Lines: {', '.join(note.linked_line_ids) if note.linked_line_ids else '-'} | "
                    f"Codes: {', '.join(note.linked_item_codes) if note.linked_item_codes else '-'}",
                    wrap=920,
                )
                dpg.add_text((note.clinical_text or "")[:220], wrap=920)
                if retrieval is None or not retrieval.results:
                    dpg.add_text("Không có chunk retrieve.", color=(148, 163, 184))
                    continue
                for hit in retrieval.results[:3]:
                    matched_codes = ", ".join(hit.matched_codes) if hit.matched_codes else "-"
                    matched_keywords = ", ".join(hit.matched_keywords) if hit.matched_keywords else "-"
                    matched_note_codes = bool(set(hit.matched_codes).intersection(set(note.linked_item_codes)))
                    dpg.add_text(
                        f"Top {hit.rank} | {hit.chunk_id} | score {hit.score:.2f}",
                        color=(37, 99, 235) if matched_note_codes else (30, 41, 59),
                    )
                    dpg.add_text(
                        f"Codes: {matched_codes} | Keywords: {matched_keywords}",
                        wrap=920,
                        color=(37, 99, 235) if matched_note_codes else (71, 85, 105),
                    )

    def export_xml5_retrieval_json() -> None:
        latest = state["last_xml5_retrieval_result"]
        if latest is None:
            set_status("Chưa có XML5 retrieval preview để export.", (220, 38, 38))
            return
        export_raw = get_value(TAG_XML5_RETRIEVAL_EXPORT).strip()
        if not export_raw:
            set_status("Cần nhập đường dẫn file export XML5 retrieval JSON.", (220, 38, 38))
            return
        export_path = ensure_runtime_path(export_raw)
        payload = {
            "xml_file": str(latest.xml_file),
            "effective_date": latest.effective_date,
            "note_records": [asdict(note) for note in latest.note_records],
            "retrieval_results": [asdict(result) for result in latest.retrieval_results],
        }
        export_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n",
            encoding="utf-8",
        )
        set_status(f"Đã export XML5 retrieval JSON ra {export_path}.", (22, 163, 74))

    def render_diagnosis_validation(result: PreviewRunResult | None) -> None:
        clear_container(TAG_DIAGNOSIS_CONTAINER)
        if result is None or not result.diagnosis_validation_results:
            dpg.set_value(TAG_DIAGNOSIS_SUMMARY, "Chưa có kết quả đối chiếu chẩn đoán.")
            return

        validations = result.diagnosis_validation_results
        dpg.set_value(
            TAG_DIAGNOSIS_SUMMARY,
            f"Đối chiếu chẩn đoán | {len(validations)} mã | "
            + ", ".join(
                f"{item.diagnosis_code}:{item.validation_status}"
                for item in validations
            ),
        )
        for item in validations:
            with dpg.child_window(parent=TAG_DIAGNOSIS_CONTAINER, border=True, height=160, autosize_x=True):
                dpg.add_text(
                    f"{item.diagnosis_code} | {item.validation_status}",
                    color=diagnosis_status_color(item.validation_status),
                )
                dpg.add_text(
                    f"Profile: {item.profile_id or '-'} | Gợi ý xử lý: {item.recommended_action}",
                    color=(30, 41, 59),
                )
                dpg.add_text(item.summary or "-", wrap=920)
                dpg.add_text(
                    f"Matched symptoms: {', '.join(item.matched_symptoms) if item.matched_symptoms else '-'}",
                    wrap=920,
                    color=(22, 101, 52),
                )
                dpg.add_text(
                    f"Matched tests/codes: {', '.join(item.matched_tests) if item.matched_tests else '-'}",
                    wrap=920,
                    color=(37, 99, 235),
                )
                if item.missing_evidence:
                    dpg.add_text(
                        f"Thiếu chứng cứ: {', '.join(item.missing_evidence)}",
                        wrap=920,
                        color=(234, 88, 12),
                    )
                if item.conflicting_evidence:
                    dpg.add_text(
                        f"Xung đột/chống chỉ định: {', '.join(item.conflicting_evidence)}",
                        wrap=920,
                        color=(185, 28, 28),
                    )

    def load_rule_into_form(rule: RuleEditorRecord) -> None:
        state["selected_rule_id"] = rule.rule_id
        dpg.set_value(TAG_RULE_ID, rule.rule_id)
        dpg.set_value(TAG_RULE_NAME, rule.rule_name)
        dpg.set_value(TAG_RULE_GROUP, rule.rule_group)
        set_combo_value(TAG_SEVERITY, rule.severity, SEVERITY_LABELS)
        set_combo_value(TAG_INPUT_SCOPE, rule.input_scope, INPUT_SCOPE_LABELS)
        set_combo_value(TAG_SUGGESTED_ACTION, rule.suggested_action, SUGGESTED_ACTION_LABELS)
        dpg.set_value(TAG_LEGAL_BASIS, rule.legal_basis)
        dpg.set_value(TAG_OWNER, rule.owner)
        dpg.set_value(TAG_EFFECTIVE_FROM, rule.effective_from)
        dpg.set_value(TAG_EFFECTIVE_TO, rule.effective_to or "")
        dpg.set_value(TAG_ENABLED, rule.enabled)
        dpg.set_value(TAG_DECISION_LOGIC, rule.decision_logic)

    def filtered_rules() -> list[RuleEditorRecord]:
        keyword = get_value(TAG_SEARCH).strip().lower()
        rules = current_rules()
        if not keyword:
            return rules
        return [
            rule
            for rule in rules
            if keyword in rule.rule_id.lower()
            or keyword in rule.rule_name.lower()
            or keyword in rule.rule_group.lower()
        ]

    def refresh_rule_list() -> None:
        clear_container(TAG_RULE_LIST)
        with dpg.group(parent=TAG_RULE_LIST):
            for rule in filtered_rules():
                status_label = "Dang bat" if rule.enabled else "Dang tat"
                summary = " | ".join(
                    [
                        rule.rule_group,
                        display_value(rule.severity, SEVERITY_LABELS),
                        display_value(rule.input_scope, INPUT_SCOPE_LABELS),
                    ]
                )
                with dpg.child_window(border=True, height=110, autosize_x=True):
                    dpg.add_text(rule.rule_id)
                    dpg.add_text(rule.rule_name)
                    dpg.add_text(summary)
                    dpg.add_text(status_label, color=(22, 163, 74) if rule.enabled else (220, 38, 38))
                    dpg.add_button(
                        label="Chỉnh rule này",
                        callback=lambda s, a, u=rule: load_rule_into_form(u),
                    )

    def save_current_rule() -> None:
        selected_rule_id = state["selected_rule_id"]
        if not selected_rule_id:
            set_status("Chưa chọn rule để lưu.", (220, 38, 38))
            return
        updated_rule = RuleEditorRecord(
            rule_id=get_value(TAG_RULE_ID),
            rule_name=get_value(TAG_RULE_NAME),
            rule_group=get_value(TAG_RULE_GROUP),
            severity=get_combo_key(TAG_SEVERITY, SEVERITY_LABELS, SEVERITY_KEYS_BY_LABEL) or "warning",
            legal_basis=get_value(TAG_LEGAL_BASIS),
            effective_from=get_value(TAG_EFFECTIVE_FROM),
            effective_to=get_value(TAG_EFFECTIVE_TO).strip() or None,
            input_scope=get_combo_key(TAG_INPUT_SCOPE, INPUT_SCOPE_LABELS, INPUT_SCOPE_KEYS_BY_LABEL) or "line",
            decision_logic=get_value(TAG_DECISION_LOGIC),
            suggested_action=(
                get_combo_key(TAG_SUGGESTED_ACTION, SUGGESTED_ACTION_LABELS, SUGGESTED_ACTION_KEYS_BY_LABEL)
                or "warn"
            ),
            owner=get_value(TAG_OWNER),
            enabled=bool(dpg.get_value(TAG_ENABLED)),
        )
        service.update_rule(updated_rule)
        refresh_rule_list()
        set_status(f"Đã lưu rule {updated_rule.rule_id}.", (22, 163, 74))

    def toggle_selected_rule() -> None:
        if not state["selected_rule_id"]:
            set_status("Chưa chọn rule để bật/tắt.", (220, 38, 38))
            return
        current_enabled = bool(dpg.get_value(TAG_ENABLED))
        dpg.set_value(TAG_ENABLED, not current_enabled)

    def save_payment_policy() -> None:
        if PAYMENT_POLICY_FILE is None:
            set_status("Chưa cấu hình file payment policy.", (220, 38, 38))
            return
        updated_payment_policy = PaymentPolicyRecord(
            source_ref=get_value(TAG_PAYMENT_SOURCE).strip() or "payment-policy@0.1.0",
            included_in_price_codes={
                "service": parse_list_field(get_value(TAG_PAYMENT_SERVICE_CODES)),
                "drug": parse_list_field(get_value(TAG_PAYMENT_DRUG_CODES)),
                "supply": parse_list_field(get_value(TAG_PAYMENT_SUPPLY_CODES)),
            },
            included_in_price_keywords={
                "service": parse_list_field(get_value(TAG_PAYMENT_SERVICE_KEYWORDS)),
                "drug": parse_list_field(get_value(TAG_PAYMENT_DRUG_KEYWORDS)),
                "supply": parse_list_field(get_value(TAG_PAYMENT_SUPPLY_KEYWORDS)),
            },
        )
        service.save_payment_policy(updated_payment_policy)
        set_status("Đã lưu payment policy.", (22, 163, 74))

    def save_clinical_policy() -> None:
        if CLINICAL_POLICY_FILE is None:
            set_status("Chưa cấu hình file clinical policy.", (220, 38, 38))
            return
        try:
            payload = json.loads(get_value(TAG_CLINICAL_JSON) or "{}")
        except json.JSONDecodeError as exc:
            set_status(f"Clinical policy JSON không hợp lệ: {exc}", (220, 38, 38))
            return
        updated_clinical_policy = ClinicalPolicyRecord(
            source_ref=get_value(TAG_CLINICAL_SOURCE).strip() or "clinical-policy@0.1.0",
            payload=payload,
        )
        service.save_clinical_policy(updated_clinical_policy)
        dpg.set_value(
            TAG_CLINICAL_JSON,
            json.dumps(updated_clinical_policy.to_dict(), ensure_ascii=False, indent=2),
        )
        set_status("Đã lưu clinical policy.", (22, 163, 74))

    def render_preview(result: PreviewRunResult) -> None:
        state["last_preview_result"] = result
        render_diagnosis_validation(result)
        clear_container(TAG_PREVIEW_GROUPS)
        clear_container(TAG_PREVIEW_HITS)
        related_notes_by_line = note_map_by_line_id()
        filtered_note = selected_xml5_note()
        dpg.set_value(
            TAG_PREVIEW_SUMMARY,
            f"Ho so {result.claim.header.claim_id} | "
            f"{len(result.claim.lines)} dong | "
            f"{len(result.engine_result.hits)} hit | "
            f"Phan luong: {result.triage_result.triage_level} | "
            f"Rule hieu luc: {result.effective_rule_count} | "
            f"Guideline draft: {result.guideline_draft_count}",
        )

        if not result.engine_result.hits:
            with dpg.group(parent=TAG_PREVIEW_GROUPS, horizontal=True):
                button = dpg.add_button(label="Không có hit", enabled=False)
                dpg.bind_item_theme(button, BADGE_THEME_TAGS["info"])
            dpg.add_text(
                "Không có rule hit trên file XML này.",
                parent=TAG_PREVIEW_HITS,
                color=(22, 163, 74),
            )
            return

        grouped_hits: dict[str, list[object]] = {key: [] for key in PREVIEW_GROUP_ORDER}
        for hit in result.engine_result.hits:
            if filtered_note is not None and hit.line_id not in filtered_note.linked_line_ids:
                continue
            grouped_hits.setdefault(preview_group_key(hit.rule_id), []).append(hit)

        def apply_preview_group_filter(group_key: str) -> None:
            state["selected_preview_group"] = group_key
            latest = state["last_preview_result"]
            if latest is not None:
                render_preview(latest)

        all_hits = list(result.engine_result.hits)
        if filtered_note is not None:
            all_hits = [hit for hit in all_hits if hit.line_id in filtered_note.linked_line_ids]
        all_total_impact = sum((hit.estimated_amount_impact or 0) for hit in all_hits)
        severity_counts = {"reject": 0, "pending": 0, "warning": 0, "info": 0}
        for hit in all_hits:
            severity_key = str(getattr(hit, "severity", "")).lower()
            severity_counts[severity_key] = severity_counts.get(severity_key, 0) + 1

        with dpg.group(parent=TAG_PREVIEW_HITS, horizontal=True):
            for severity_key in ["reject", "pending", "warning", "info"]:
                count = severity_counts.get(severity_key, 0)
                if count == 0:
                    continue
                impact = sum(
                    (getattr(hit, "estimated_amount_impact", 0) or 0)
                    for hit in all_hits
                    if str(getattr(hit, "severity", "")).lower() == severity_key
                )
                with dpg.child_window(border=True, height=76, width=240):
                    dpg.add_text(
                        severity_panel_title(severity_key),
                        color=severity_color(severity_key),
                    )
                    dpg.add_text(f"So luong: {count}", color=(30, 41, 59))
                    dpg.add_text(
                        f"Tac dong uoc tinh: {format_amount(impact)}",
                        color=(71, 85, 105),
                    )
        dpg.add_separator(parent=TAG_PREVIEW_HITS)
        with dpg.group(parent=TAG_PREVIEW_GROUPS, horizontal=True):
            all_button = dpg.add_button(
                label=f"ALL: {len(all_hits)} | {format_amount(all_total_impact)}",
                callback=lambda s, a, u=PREVIEW_GROUP_ALL: apply_preview_group_filter(u),
            )
            dpg.bind_item_theme(
                all_button,
                BADGE_THEME_TAGS["selected"]
                if state["selected_preview_group"] == PREVIEW_GROUP_ALL
                else BADGE_THEME_TAGS["default"],
            )
            for group_key in PREVIEW_GROUP_ORDER:
                group_hits = grouped_hits.get(group_key, [])
                if not group_hits:
                    continue
                total_impact = sum((hit.estimated_amount_impact or 0) for hit in group_hits)
                button = dpg.add_button(
                    label=f"{group_key}: {len(group_hits)} | {format_amount(total_impact)}",
                    callback=lambda s, a, u=group_key: apply_preview_group_filter(u),
                )
                dpg.bind_item_theme(
                    button,
                    badge_theme_for_group(
                        group_key,
                        str(state["selected_preview_group"]),
                        group_hits,
                    ),
                )

        for group_key in PREVIEW_GROUP_ORDER:
            group_hits = grouped_hits.get(group_key, [])
            if not group_hits:
                continue
            if state["selected_preview_group"] not in {PREVIEW_GROUP_ALL, group_key}:
                continue
            sorted_hits = sorted(
                group_hits,
                key=lambda hit: (
                    severity_sort_key(getattr(hit, "severity", "")),
                    -float(getattr(hit, "estimated_amount_impact", 0) or 0),
                    str(getattr(hit, "rule_id", "")),
                    str(getattr(hit, "line_id", "")),
                ),
            )
            dpg.add_separator(parent=TAG_PREVIEW_HITS)
            dpg.add_text(
                f"{PREVIEW_GROUP_TITLES[group_key]} | {len(sorted_hits)} hit",
                parent=TAG_PREVIEW_HITS,
                color=(30, 41, 59),
            )
            if filtered_note is not None:
                dpg.add_text(
                    f"Dang loc theo XML5 note: {filtered_note.note_id}",
                    parent=TAG_PREVIEW_HITS,
                    color=(234, 88, 12),
                )
            for hit in sorted_hits:
                with dpg.child_window(parent=TAG_PREVIEW_HITS, border=True, height=190, autosize_x=True):
                    dpg.add_text(
                        severity_panel_title(getattr(hit, "severity", "")),
                        color=severity_color(getattr(hit, "severity", "")),
                    )
                    dpg.add_text(
                        f"{hit.rule_id} | {display_value(hit.severity, SEVERITY_LABELS)}",
                    )
                    dpg.add_text(
                        f"Van de: {hit_problem_label(hit)}",
                        color=(30, 41, 59),
                    )
                    dpg.add_text(
                        f"Dòng: {hit.line_id or '-'} | Gợi ý xử lý: "
                        f"{display_value(hit.suggested_action, SUGGESTED_ACTION_LABELS)} | "
                        f"Số tiền: {format_amount(hit.estimated_amount_impact or 0)}"
                    )
                    dpg.add_text("Mo ta loi/van de:", color=(71, 85, 105))
                    dpg.add_text(hit.message, wrap=900)
                    if preview_group_key(hit.rule_id) == "GUIDELINE":
                        dpg.add_text(
                            f"Thiếu chứng cứ: {', '.join(hit.required_evidence) if hit.required_evidence else '-'}",
                            wrap=900,
                            color=(234, 88, 12),
                        )
                    elif hit.required_evidence:
                        dpg.add_text(
                            f"Can doi chieu them: {', '.join(hit.required_evidence)}",
                            wrap=900,
                            color=(202, 138, 4),
                        )
                    if hit.line_id and hit.line_id in related_notes_by_line:
                        related_notes = related_notes_by_line[hit.line_id][:3]
                        related_label = " | ".join(
                            f"{note.note_id} ({note.note_type})"
                            for note in related_notes
                        )
                        dpg.add_text(
                            f"XML5 note liên quan: {related_label}",
                            wrap=900,
                            color=(37, 99, 235),
                        )

    def run_preview() -> None:
        xml_raw = get_value(TAG_PREVIEW_XML).strip()
        effective_date = get_value(TAG_PREVIEW_DATE).strip()
        if not xml_raw:
            set_status("Cần nhập đường dẫn file XML.", (220, 38, 38))
            return
        xml_file = Path(xml_raw)
        if not xml_file.exists():
            set_status(f"Không tìm thấy file XML: {xml_file}", (220, 38, 38))
            return
        if not effective_date:
            set_status("Cần nhập ngày hiệu lực.", (220, 38, 38))
            return
        dpg.set_value(TAG_PREVIEW_SUMMARY, "Đang chạy thử rule...")
        dpg.set_value(TAG_XML5_RETRIEVAL_SUMMARY, "Đang chạy XML5 retrieval...")
        dpg.set_value(TAG_DIAGNOSIS_SUMMARY, "Đang đối chiếu chẩn đoán...")
        clear_container(TAG_PREVIEW_GROUPS)
        clear_container(TAG_PREVIEW_HITS)
        clear_container(TAG_XML5_RETRIEVAL_CONTAINER)
        clear_container(TAG_DIAGNOSIS_CONTAINER)
        try:
            preview_result = service.run_preview(xml_file, effective_date)
        except Exception as exc:
            dpg.set_value(TAG_PREVIEW_SUMMARY, f"Chạy thử thất bại: {exc}")
            dpg.set_value(TAG_XML5_RETRIEVAL_SUMMARY, "XML5 retrieval chưa chạy.")
            dpg.set_value(TAG_DIAGNOSIS_SUMMARY, "Đối chiếu chẩn đoán chưa chạy.")
            set_status("Không thể chạy thử rule trên file XML.", (220, 38, 38))
            return
        render_preview(preview_result)
        try:
            retrieval_preview = service.run_xml5_retrieval_preview(xml_file, effective_date)
        except Exception as exc:
            render_xml5_retrieval(None)
            dpg.set_value(
                TAG_XML5_RETRIEVAL_SUMMARY,
                f"XML5 retrieval chưa sẵn sàng: {exc}",
            )
        else:
            render_xml5_retrieval(retrieval_preview)
            render_preview(preview_result)
        set_status(f"Đã chạy thử rule trên {preview_result.xml_file.name}.", (22, 163, 74))

    def export_preview_json() -> None:
        last_preview_result = state["last_preview_result"]
        if last_preview_result is None:
            set_status("Chưa có kết quả preview để export.", (220, 38, 38))
            return
        export_raw = get_value(TAG_PREVIEW_EXPORT).strip()
        if not export_raw:
            set_status("Cần nhập đường dẫn file export JSON.", (220, 38, 38))
            return
        export_path = ensure_runtime_path(export_raw)
        selected_preview_group = str(state["selected_preview_group"])
        if selected_preview_group == PREVIEW_GROUP_ALL:
            filtered_hits = list(last_preview_result.engine_result.hits)
        else:
            filtered_hits = [
                hit
                for hit in last_preview_result.engine_result.hits
                if preview_group_key(hit.rule_id) == selected_preview_group
            ]
        payload = {
            "xml_file": str(last_preview_result.xml_file),
            "effective_date": last_preview_result.effective_date,
            "selected_preview_group": selected_preview_group,
            "claim": asdict(last_preview_result.claim),
            "engine_result": {
                "claim_id": last_preview_result.engine_result.claim_id,
                "hits": [asdict(hit) for hit in filtered_hits],
            },
            "triage_result": asdict(last_preview_result.triage_result),
            "effective_rule_count": last_preview_result.effective_rule_count,
            "guideline_draft_count": last_preview_result.guideline_draft_count,
            "diagnosis_validation_results": [
                asdict(item) for item in (last_preview_result.diagnosis_validation_results or [])
            ],
        }
        export_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n",
            encoding="utf-8",
        )
        set_status(
            f"Đã export preview JSON ({selected_preview_group}) ra {export_path}.",
            (22, 163, 74),
        )

    def choose_xml_file(sender: str, app_data: dict, user_data: object) -> None:
        selections = app_data.get("selections", {})
        if not selections:
            return
        selected_path = next(iter(selections.values()), "")
        if selected_path:
            dpg.set_value(TAG_PREVIEW_XML, selected_path)

    dpg.create_context()
    build_themes()
    build_fonts()

    with dpg.file_dialog(
        directory_selector=False,
        show=False,
        callback=choose_xml_file,
        tag=TAG_FILE_DIALOG,
        width=900,
        height=520,
    ):
        dpg.add_file_extension(".xml", color=(0, 255, 0, 255))

    with dpg.window(
        label="Tool GĐBH - Không gian giám định",
        width=1500,
        height=960,
        no_close=True,
    ):
        dpg.add_text("", tag=TAG_STATUS)
        with dpg.tab_bar():
            with dpg.tab(label="Màn Hình Giám Định"):
                dpg.add_text("Chạy thử giám định trên 1 file XML")
                dpg.add_input_text(
                    tag=TAG_PREVIEW_XML,
                    label="File XML cần chạy thử",
                    default_value=str(DEFAULT_XML_FILE) if DEFAULT_XML_FILE is not None else "",
                    width=900,
                )
                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Chọn file XML",
                        callback=lambda s, a, u=None: dpg.show_item(TAG_FILE_DIALOG),
                    )
                    dpg.add_input_text(
                        tag=TAG_PREVIEW_DATE,
                        label="Ngày hiệu lực",
                        default_value="2026-03-30",
                        width=180,
                    )
                    dpg.add_button(
                        label="Chạy thử",
                        callback=lambda s, a, u=None: run_preview(),
                    )
                with dpg.group(horizontal=True):
                    dpg.add_input_text(
                        tag=TAG_PREVIEW_EXPORT,
                        label="File JSON export",
                        default_value=str(PROJECT_ROOT / "runtime" / "preview-export.json"),
                        width=900,
                    )
                    dpg.add_button(
                        label="Export JSON",
                        callback=lambda s, a, u=None: export_preview_json(),
                    )
                dpg.add_text("Chưa chạy thử rule.", tag=TAG_PREVIEW_SUMMARY)
                dpg.add_group(tag=TAG_PREVIEW_GROUPS, horizontal=True)
                dpg.add_child_window(tag=TAG_PREVIEW_HITS, height=320, border=True)
                dpg.add_separator()
                dpg.add_text("Đối chiếu chẩn đoán chưa chạy.", tag=TAG_DIAGNOSIS_SUMMARY)
                dpg.add_child_window(tag=TAG_DIAGNOSIS_CONTAINER, height=220, border=True)
                dpg.add_separator()
                with dpg.group(horizontal=True):
                    dpg.add_input_text(
                        tag=TAG_XML5_RETRIEVAL_EXPORT,
                        label="File XML5 retrieval export",
                        default_value=str(PROJECT_ROOT / "runtime" / "xml5-retrieval-preview.json"),
                        width=900,
                    )
                    dpg.add_button(
                        label="Export XML5 retrieval",
                        callback=lambda s, a, u=None: export_xml5_retrieval_json(),
                    )
                dpg.add_text("XML5 retrieval chưa chạy.", tag=TAG_XML5_RETRIEVAL_SUMMARY)
                dpg.add_child_window(tag=TAG_XML5_RETRIEVAL_CONTAINER, height=340, border=True)

            with dpg.tab(label="Màn Hình Cài Đặt Rule"):
                with dpg.group(horizontal=True):
                    with dpg.child_window(width=420, autosize_y=True, border=True):
                        dpg.add_text("Danh sách rule")
                        dpg.add_input_text(
                            tag=TAG_SEARCH,
                            hint="Tìm rule theo ID / tên / nhóm",
                            callback=lambda s, a, u=None: refresh_rule_list(),
                        )
                        dpg.add_spacer(height=4)
                        dpg.add_text(f"File rule: {RULE_FILE}", wrap=390)
                        dpg.add_separator()
                        dpg.add_child_window(tag=TAG_RULE_LIST, autosize_x=True, height=760, border=False)

                    with dpg.child_window(autosize_x=True, autosize_y=True, border=True):
                        dpg.add_text("Chi tiết rule")
                        dpg.add_input_text(tag=TAG_RULE_ID, label="Rule ID", readonly=True)
                        dpg.add_input_text(tag=TAG_RULE_NAME, label="Tên rule")
                        dpg.add_input_text(tag=TAG_RULE_GROUP, label="Nhóm rule")
                        dpg.add_combo(
                            list(SEVERITY_LABELS.values()),
                            tag=TAG_SEVERITY,
                            label="Mức độ xử lý",
                        )
                        dpg.add_combo(
                            list(INPUT_SCOPE_LABELS.values()),
                            tag=TAG_INPUT_SCOPE,
                            label="Phạm vi áp dụng",
                        )
                        dpg.add_combo(
                            list(SUGGESTED_ACTION_LABELS.values()),
                            tag=TAG_SUGGESTED_ACTION,
                            label="Hướng xử lý gợi ý",
                        )
                        dpg.add_input_text(tag=TAG_LEGAL_BASIS, label="Căn cứ pháp lý")
                        dpg.add_input_text(tag=TAG_OWNER, label="Người/phòng phụ trách")
                        dpg.add_input_text(tag=TAG_EFFECTIVE_FROM, label="Hiệu lực từ")
                        dpg.add_input_text(tag=TAG_EFFECTIVE_TO, label="Hiệu lực đến")
                        dpg.add_checkbox(tag=TAG_ENABLED, label="Đang bật")
                        dpg.add_input_text(
                            tag=TAG_DECISION_LOGIC,
                            label="Diễn giải logic rule",
                            multiline=True,
                            height=110,
                        )
                        with dpg.group(horizontal=True):
                            dpg.add_button(
                                label="Lưu thay đổi",
                                callback=lambda s, a, u=None: save_current_rule(),
                            )
                            dpg.add_button(
                                label="Bật / Tắt",
                                callback=lambda s, a, u=None: toggle_selected_rule(),
                            )
                        dpg.add_separator()
                        dpg.add_text("Cấu hình payment policy")
                        dpg.add_input_text(
                            tag=TAG_PAYMENT_SOURCE,
                            label="Payment policy source",
                            default_value=payment_policy.source_ref,
                        )
                        dpg.add_input_text(
                            tag=TAG_PAYMENT_SERVICE_CODES,
                            label="Included-in-price service codes",
                            multiline=True,
                            height=70,
                            default_value=join_list_field(payment_policy.included_in_price_codes.get("service", [])),
                        )
                        dpg.add_input_text(
                            tag=TAG_PAYMENT_DRUG_CODES,
                            label="Included-in-price drug codes",
                            multiline=True,
                            height=70,
                            default_value=join_list_field(payment_policy.included_in_price_codes.get("drug", [])),
                        )
                        dpg.add_input_text(
                            tag=TAG_PAYMENT_SUPPLY_CODES,
                            label="Included-in-price supply codes",
                            multiline=True,
                            height=70,
                            default_value=join_list_field(payment_policy.included_in_price_codes.get("supply", [])),
                        )
                        dpg.add_input_text(
                            tag=TAG_PAYMENT_SERVICE_KEYWORDS,
                            label="Included-in-price service keywords",
                            multiline=True,
                            height=70,
                            default_value=join_list_field(
                                payment_policy.included_in_price_keywords.get("service", [])
                            ),
                        )
                        dpg.add_input_text(
                            tag=TAG_PAYMENT_DRUG_KEYWORDS,
                            label="Included-in-price drug keywords",
                            multiline=True,
                            height=70,
                            default_value=join_list_field(
                                payment_policy.included_in_price_keywords.get("drug", [])
                            ),
                        )
                        dpg.add_input_text(
                            tag=TAG_PAYMENT_SUPPLY_KEYWORDS,
                            label="Included-in-price supply keywords",
                            multiline=True,
                            height=70,
                            default_value=join_list_field(
                                payment_policy.included_in_price_keywords.get("supply", [])
                            ),
                        )
                        dpg.add_button(
                            label="Lưu payment policy",
                            callback=lambda s, a, u=None: save_payment_policy(),
                        )
                        dpg.add_separator()
                        dpg.add_text("Cấu hình clinical policy")
                        dpg.add_input_text(
                            tag=TAG_CLINICAL_SOURCE,
                            label="Clinical policy source",
                            default_value=clinical_policy.source_ref,
                        )
                        dpg.add_input_text(
                            tag=TAG_CLINICAL_JSON,
                            label="Clinical policy JSON",
                            multiline=True,
                            height=320,
                            default_value=json.dumps(clinical_policy.to_dict(), ensure_ascii=False, indent=2),
                        )
                        dpg.add_button(
                            label="Lưu clinical policy",
                            callback=lambda s, a, u=None: save_clinical_policy(),
                        )

            with dpg.tab(label="Màn Hình Thiết Lập Giám Định"):
                dpg.add_text(
                    "Thiết lập thông tin giám định và nguồn dữ liệu vận hành: nhân lực, thuốc, VTYT, trang thiết bị, dịch vụ, policy và knowledge-base.",
                    wrap=980,
                    color=(71, 85, 105),
                )
                dpg.add_child_window(tag=TAG_SETUP_CONTAINER, height=820, border=True)

    refresh_rule_list()
    render_setup_overview()
    first_rule = next(iter(current_rules()), None)
    if first_rule is not None:
        load_rule_into_form(first_rule)

    dpg.create_viewport(title="Tool GĐBH - Không gian giám định", width=1520, height=960)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    build_app()
