def formato_tamanho(bytes_num: int) -> str:
    """Retorna string legível do tamanho (ex: '12.3 KB')."""
    for unit in ('B','KB','MB','GB','TB'):
        if bytes_num < 1024:
            return f"{bytes_num:.1f} {unit}"
        bytes_num /= 1024
    return f"{bytes_num:.1f} PB"