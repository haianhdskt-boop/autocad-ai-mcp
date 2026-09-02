"""Knowledge Engine for AutoCAD AI Architect Suite.

Direct in-code extraction and search across all 7 architectural knowledge domains:
1. 01-tieu-chuan-khong-gian (Living, Kitchen, Bath/WC, Bedroom, Stairs/Corridor, Foyer/Study, Lightwell, Garage)
2. 02-ky-thuat-ket-cau-vat-lieu (RC Structure, Finishes, Detailing, Waterproofing)
3. 03-he-thong-mep-dien-nuoc (Electrical/Lighting, Plumbing/Drainage, HVAC, Child Safety/PCCC)
4. 04-thiet-ke-khi-hau-ben-vung (Tropical monsoon design, Passive Cooling, Insulation)
5. 05-thiet-ke-tiep-can-da-dung (Elderly accessibility, Wheelchair universal design)
6. 06-nguyen-ly-tham-my-tao-hinh (Golden ratio, Color psychology 60-30-10, 8 Styles, Quality rubric)
7. 07-du-toan-va-quan-ly-du-an (BOQ, Investment rates, Client profiles, AI rendering prompts)
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional

LIBRARY_DIR = Path(__file__).parent / "library"


def get_library_topics() -> List[Dict[str, Any]]:
    """Liệt kê toàn bộ các chuyên đề hướng dẫn kiến trúc có trong thư viện mã nguồn."""
    topics = []
    if not LIBRARY_DIR.exists():
        return topics

    for folder in sorted(LIBRARY_DIR.iterdir()):
        if folder.is_dir() and not folder.name.startswith("."):
            docs = []
            for file in sorted(folder.glob("*.md")):
                docs.append({
                    "slug": file.stem,
                    "filename": file.name,
                    "path": str(file),
                })
            topics.append({
                "category": folder.name,
                "documents_count": len(docs),
                "documents": docs,
            })
    return topics


def get_full_topic_document(topic_slug_or_filename: str) -> Optional[Dict[str, Any]]:
    """Trích xuất toàn bộ nội dung hướng dẫn chi tiết của 1 tài liệu theo tên chuyên đề."""
    clean_slug = topic_slug_or_filename.strip().lower().replace("_", "-").replace(".md", "")
    
    if not LIBRARY_DIR.exists():
        return None

    # Search directly for file
    for md_file in LIBRARY_DIR.rglob("*.md"):
        if md_file.stem.lower() == clean_slug or md_file.name.lower() == clean_slug:
            try:
                content = md_file.read_text(encoding="utf-8")
                return {
                    "slug": md_file.stem,
                    "filename": md_file.name,
                    "category": md_file.parent.name,
                    "content": content,
                }
            except Exception as e:
                return {"error": str(e)}

    # Fuzzy match
    for md_file in LIBRARY_DIR.rglob("*.md"):
        if clean_slug in md_file.stem.lower():
            try:
                content = md_file.read_text(encoding="utf-8")
                return {
                    "slug": md_file.stem,
                    "filename": md_file.name,
                    "category": md_file.parent.name,
                    "content": content,
                }
            except Exception as e:
                return {"error": str(e)}

    return None


def search_reference_library(keyword: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Tìm kiếm nhanh từ khóa quy chuẩn trên toàn bộ kho tài liệu kiến trúc."""
    results = []
    query = keyword.strip().lower()
    if not query or not LIBRARY_DIR.exists():
        return results

    for md_file in sorted(LIBRARY_DIR.rglob("*.md")):
        if md_file.name == "README.md":
            continue
        try:
            lines = md_file.read_text(encoding="utf-8").splitlines()
            matched_snippets = []
            for idx, line in enumerate(lines):
                if query in line.lower():
                    # Get surrounding context
                    start = max(0, idx - 1)
                    end = min(len(lines), idx + 3)
                    snippet = "\n".join(lines[start:end])
                    matched_snippets.append(snippet)
                    if len(matched_snippets) >= 2:
                        break

            if matched_snippets:
                results.append({
                    "document": md_file.name,
                    "category": md_file.parent.name,
                    "snippets": matched_snippets,
                })
                if len(results) >= max_results:
                    break
        except Exception:
            continue

    return results


def get_room_guidelines(room_type: str) -> Dict[str, Any]:
    """Trích xuất nhanh các thông số công thái học và quy chuẩn không gian cho 1 phòng."""
    rtype = room_type.lower().strip()
    
    mapping = {
        "living": "phong-khach",
        "khach": "phong-khach",
        "kitchen": "bep-va-phong-an",
        "bep": "bep-va-phong-an",
        "an": "bep-va-phong-an",
        "wc": "phong-tam-ve-sinh",
        "bath": "phong-tam-ve-sinh",
        "tam": "phong-tam-ve-sinh",
        "ve_sinh": "phong-tam-ve-sinh",
        "bedroom": "phong-ngu-va-tu-ao",
        "ngu": "phong-ngu-va-tu-ao",
        "master": "phong-ngu-va-tu-ao",
        "stairs": "cau-thang-va-hanh-lang",
        "thang": "cau-thang-va-hanh-lang",
        "corridor": "cau-thang-va-hanh-lang",
        "hanh_lang": "cau-thang-va-hanh-lang",
        "foyer": "sanh-vao-va-phong-lam-viec",
        "sanh": "sanh-vao-va-phong-lam-viec",
        "study": "sanh-vao-va-phong-lam-viec",
        "lam_viec": "sanh-vao-va-phong-lam-viec",
        "lightwell": "gieng-troi-va-thong-tang",
        "gieng_troi": "gieng-troi-va-thong-tang",
        "garage": "gara-san-vuon-ban-cong",
        "gara": "gara-san-vuon-ban-cong",
        "ban_cong": "gara-san-vuon-ban-cong",
    }
    
    target_slug = mapping.get(rtype, "phong-khach")
    for k, v in mapping.items():
        if k in rtype:
            target_slug = v
            break

    doc = get_full_topic_document(target_slug)
    if doc:
        return {
            "room_type": room_type,
            "target_document": doc["filename"],
            "category": doc["category"],
            "guideline_markdown": doc["content"],
        }
    return {
        "room_type": room_type,
        "error": f"Không tìm thấy tài liệu cho phòng '{room_type}'",
    }
