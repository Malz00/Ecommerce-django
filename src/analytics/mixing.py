from .signals import object_viewed_signal

class ObjectViewedMixing(object):
    def get_Context_data(self, *args, **kwargs):
        context= super(ObjectViewedMixing, self).get_context_data(*args, **kwargs)
        request = self.request
        instance = context.get('object')
        if instance:
            object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return context
    

    
 #object_viewed_signal.send(sender=YourModelClass, instance=instance, request=request)