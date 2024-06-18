
class step:
    # All photoplugins classes that are in the event loop
    # must use this interface
    def run(self, display, events, session):
        pass
