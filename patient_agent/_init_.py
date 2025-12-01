__all__ = ["root_agent"]
def __getattr__(name):
    if name == "root_agent":
        # Lazy import to avoid circular import
        from .agent import root_agent
        return root_agent
    raise AttributeError(f"module {__name__} has no attribute {name}")
