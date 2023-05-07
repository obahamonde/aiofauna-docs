<style>
img {
  display: block;
  margin-left: auto;
  margin-right: auto;
}
</style>


# AioFauna

![Image](/static/logo.svg?100x100)

**Resources**

[GitHub](https://github.com/obahamonde/aiofauna)

[Documentation](https://obahamonde-aiofauna-docs.smartpro.solutions/)

[PyPI](https://pypi.org/project/aiofauna/)

**Features**

- **Async**. `aiofauna` is fully async, so you can use it with any async framework.
- **Document Relational Database**. `aiofauna` comes with an opinionated FaunaDB ODM (Object Document Mapper).
- **FastAPI-esque**. `aiofauna` is inspired by FastAPI, so if you are familiar with FastAPI, you will feel right at home.
- **Easy to use**. `aiofauna` is designed to be easy to use and learn. It comes with a lot of built-in functionality that requires minimal setup.
- **Performance**. `aiofauna` is designed for high performance, superior to faunadb-python and comparable to FastAPI in several use cases.
- **Integrations**. Thanks to `aiohttp.ClientSession`, AioFauna can integrate seamlessly with almost any third party data source, api, or cloud service.

**Example**

First we Install the package using pip:

```bash
pip install aiofauna
```

<hr/>

Then we create a file called `main.py` and add the following code:

```python
from aiofauna import Api, FaunaModel, Field
from uuid import uuid4

app = Api()

class Product(FaunaModel):
    name: str = Field(..., unique=True)
    price: float = Field(..., index=True)

@app.get("/products")
async def get_products():
    return await Product.find_all()

@app.post("/products")
async def create_product(product: Product):
    return await product.save()

@app.get("/products/{ref}")
async def get_product(ref: str):
    return await Product.find(ref)

@app.put("/products/{ref}")
async def update_product(ref: str, product: Product):
    return await product.update(ref,**product.dict())

@app.delete("/products/{ref}")
async def delete_product(ref: str):
    return await Product.delete(ref)

@app.on_event("startup")
async def startup(_):
    await Product.provision()

```

<hr/>

In order to use FaunaDB API we must provide `FAUNA_SECRET` environment variable, we can obtain it from `CubeCTL` platform developed by aiofauna team and hosted on [SmartPro](https://www.smartpro.solutions/).

First we go to the `/database` section and get a new database key:

![Image](/static/1.png)

<hr/>

When the key is generated we copy the secret into the clipboard and pass it to our `.env` file:

![Image](/static/2.png)

<hr/>

Our project structure should look like:

```bash
|_ main.py
|_ .env
```

<hr/>

Now we can run our development server:

```bash
adev runserver --livereload
```

<hr/>

Since we are calling `provision` method for our `Product` model on `startup` event, the `Product` collection, indexes and unique constraints are automatically created on our database.

![Image](/static/3.png)

<hr/>

Then we can visit `http://localhost:8000/docs` to see the interactive documentation and start testing our API:

![Image](/static/4.png)