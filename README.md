sanja
=====

This module aims to make bringing Jinja templates to Sanic to be easy.  

It is entirelly up to You  
how You will configure your Jinja template environment.  
Great freedom :-)  

It consist of only two dozens lines of simple code.  

# Installation.  

    pip install sanja  

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

* some\_view function has to return jinja "context" instance.  
* In first sanja.render() parameter provide jinja template.  
  (In this example it has to be under  
      some\_package/templates/some_template.html.jinja  
  because it is how we configured here jinja template environment,  
  so having any isues please refer to Jinja documentation).  
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
