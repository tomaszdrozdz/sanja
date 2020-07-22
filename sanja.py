# -*- coding: utf-8 -*-

"""This module aims to make bringing Jinja templates to Sanic to be easy.  

It is entirelly up to You  
how You will configure your Jinja template environment.  
Great freedom :-)  

# First You have to configure Your Sanic app so it holds Jinja template environment instance.  

    app = sanic.Sanic("Some app")  

    sanja_conf_app(  
        app,  
        # There go normal parameters like for jijna2.Environment(),  
        # for example:  
        auto_reload=True,  
        loader=jinja2PrefixLoader({  
            'some_package': jinja_PackageLoader("some_package")}))  

By default this Jinja template environment is held in:  

    app.config['JINJA_ENV']  

so equaly well You could do:  

    app.config['JINJA_ENV'] = jinja2.Environment(  
        auto_reload=True,  
        loader=jinja2PrefixLoader({  
            'some_package': jinja_PackageLoader("some_package")}))  

But if You wish to change it,  
or have more then one Jinja template environment,  
then just:  

    sanja_conf_app(  
        app,  
        jinja_template_env_name="JINJA_ENV_2",  
        ...)  

or:  

    app.config['JINJA_ENV_2'] = jinja2.Environment(  
        ...)  


# Then You can just use Jinja rendering and Sanic response.  

To do so simply decorate your request handler,  
for example:  

    @app.route("/some/url")  
    @sanja.render("some_package/some_template.html.jinja", "html")  
    async def some_view(request):  
        ...  
        return {'jijna': "context"}  

* some_view function has to return jinja "context" instance.  
* In first sanja.render() parameter provide jinja template.  
  (In this example it has to be under  
      some_package/templates/some_template.html.jinja  
  because it is how we configured here jinja template environment,  
  so having any issues please refer to Jinja documentation).  
* Second sanja.render() parameter coresponds to sanic.response "kind",  
  so if doubts plese refer to Sanic documentation.  
  Possible values are:  
  * "text"  
  * "html"  
  * "json"  
  * "raw"  

And if You want to use other Jinja template environment,  
that You have configured before,  
you can do so:  

    @app.route("/some/url2")  
    @sanja.render("some_package/some_template.html.jinja", "html", jinja_template_env_name="JINJA_ENV_2")  
    async def some_view(request):  
        ...  
        return {'jijna': "context"}  

# Yo can also use it for Class-Based Views.  

in decorators class variable:  

    class YourView(sanic.views.HTTPMethodView):  
        decorators = [sanja.render(...)]  
    
        ...  

or per http method:  

    class YourView(sanic.views.HTTPMethodView):  
    
        @sanja.render(...)  
        async def get(self, request):  
            ...  
    
        ...  
"""  



from functools import wraps

from jinja2 import Environment as jinja_Environment

from sanic.response import text as sanic_response_text, \
                           html as sanic_response_html, \
                           json as sanic_response_json, \
                           raw  as sanic_response_raw



__version__ = "1.0.1"
__author__ = "tomaszdrozdz"
__author_email__ = "tomasz.drozdz.1@protonmail.com"



def conf_app(app, jinja_template_env_name="JINJA_ENV", *args, **kwargs):
    """Create Jinja template environment, and srotes it in sanic app.config.  


    Parameters
    ----------
    app: sanic app instance  
    jinja_template_env_name:  str, optional  
        jinja template environment instance will be held under  
        app.config[jinja_template_env_name].  
        This also coresponds to  
        jinja_template_env_name in render() function.  
    *args, **kwargs:  
        are just jijna2.Environment() parameters.  

    Returns
    -------
    created Jinja environment template instance."""

    jinja_template_environment = jinja_Environment(*args, **kwargs)
    app.config[jinja_template_env_name] = jinja_template_environment
    return jinja_template_environment


def render(template, render_as, jinja_template_env_name='JINJA_ENV'):
    """Decorator for Sanic request handler,  

    that turns it into function returning generated jinja template.  

    Decorated function (or method) has to return jinja "context" instance.  

    Parameters:
    -----------
    template:  str  
        jinja template name.  
    render_as: str  
        corresponds to sanic.response "kind".  
        Possible valuse are: "text", "html", "json", "raw".  
    jinja_template_env_name:  str, optional
        Where jinja template environment instance is held in  
        app.config.  
        This coresponds to  
        jinja_template_env_name in conf_app() function."""

    _jinja_renderers = {
        'text': sanic_response_text,
        'html': sanic_response_html,
        'json': sanic_response_json,
        'raw':  sanic_response_raw }

    def _decorator(to_decorate):

        @wraps(to_decorate)
        async def _decorated(*args, **kwargs):

            request = args[-1]
            _jinja_env = request.app.config[jinja_template_env_name]

            template_context = await to_decorate(*args, **kwargs)

            if _jinja_env.enable_async:
                rendered_template = await _jinja_env.get_template(template).render_async(template_context)
            else:
                rendered_template = _jinja_env.get_template(template).render(template_context)

            return _jinja_renderers[render_as](rendered_template)

        return _decorated

    return _decorator
