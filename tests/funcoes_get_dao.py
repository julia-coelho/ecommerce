#Aluna: Júlia Coelho Rodrigues
#RA: 22408388


def get_cat(conexao, id):
    from dao.category_dao import CategoryDAO
    cat_dao = CategoryDAO(conexao)
    found, cat = cat_dao.find_by_id(id)
    return cat if found else None


def get_prod(conexao, id):
    from dao.product_dao import ProductDAO
    prod_dao = ProductDAO(conexao)
    found, prod = prod_dao.find_by_id(id)
    return prod if found else None


def get_cust(conexao, id):
    from dao.customer_dao import CustomerDAO
    cust_dao = CustomerDAO(conexao)
    found, cust = cust_dao.find_by_id(id)
    return cust if found else None


def get_order(conexao, id):
    from dao.order_dao import OrderDAO
    order_dao = OrderDAO(conexao)
    found, order = order_dao.find_by_id(id)
    return order if found else None