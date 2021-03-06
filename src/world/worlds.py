def world_needed(cls):
    for attr in cls.__dict__:
        if callable(getattr(cls, attr)) and '_' not in attr:
            def decorator(f):
                def wrapper(*args, **kwargs):
                    if isinstance(args[0], cls) and args[0].world is None:
                        raise ValueError('Renderer can not be used without attaching it to world.')

                    return f(*args, **kwargs)
                
                return wrapper

            setattr(cls, attr, decorator(getattr(cls, attr)))
    return cls
    

class World:
    def __init__(self, width=None, height=None):
        self._width = width
        self._height = height
        self._models = []
        self._renderer = None
        self._camera = None

    @property
    def camera(self):
    	return self._camera

    @camera.setter
    def camera(self, value):
        self._camera = value
        self._camera.world = self

    @property
    def renderer(self):
    	return self._renderer

    @renderer.setter
    def renderer(self, value):
        self._renderer = value
        self._renderer.world = self
    
    @property
    def models(self):
    	return self._models
    

    def add_model(self, model):
        self._models.append(model)

    def clear(self):
        return self._renderer.clear()

    def update(self):
        for model in self._models:
            model.update()

    def render(self):
        self._renderer.render()

    def show(self):
        self._renderer.show()
    