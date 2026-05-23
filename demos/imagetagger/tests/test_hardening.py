from imagetagger.constants import ALLOWED_CONTENT_TYPES, MAX_UPLOAD_BYTES


def test_upload_size_limit_is_reasonable():
    # Big enough for normal phone-camera JPEGs, small enough that a
    # process can decode it without running out of memory.
    assert 1 * 1024 * 1024 <= MAX_UPLOAD_BYTES <= 50 * 1024 * 1024


def test_allowed_content_types_match_frontend_input_accept():
    # Frontend <input accept="image/jpeg, image/png"> - the server-side
    # allowlist must match or stricter, otherwise the UX silently
    # diverges from what the server accepts.
    assert ALLOWED_CONTENT_TYPES == frozenset({"image/jpeg", "image/png"})
