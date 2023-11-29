def define_env(env):
    """
    This is the hook for the functions (new form)
    """

    @env.macro
    def hello():
        return 1