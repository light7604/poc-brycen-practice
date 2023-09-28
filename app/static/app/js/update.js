var updateBtns = document.getElementsByClassName('update-cart')
// var countBtns = document.getElementById('order-count')

for (i=0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click',function() {
        var productId = this.dataset.product
        var action = this.dataset.action
        // console.log('producIt', productId,'action',action)
        // console.log('user',user)
        if (user === "AnonymousUser") {
            console.log('user not logged in')
        } else {
            // console.log('csrftoken',csrftoken)
            updateUserOrder(productId, action, 0)
        }
    })
}

function updateUserOrder(productId, action, value){
    // console.log('user logged in, success add')
    if (action == 'add2') {
        value = parseInt(document.getElementById('order-count').value)
    }

    var url = '/update_item/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'producId': productId,'action': action, 'value': value})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        // console.log('data:',data)
        location.reload()
    })
}

function searchProduct(page = 1, category = "") {
    var stringQuery = ""
    var size = document.getElementById('id_size_product').value
    var search = document.getElementById('id_search_product').value
    var sort = document.getElementById('id_sort_product').value
    
    if (size.length = 0) {
        stringQuery += "&size=3"
    } else {
        stringQuery += "&size=" + size
    }

    if (category != '') {
        stringQuery += "&category=" + category
    }

    if (search.length != 0) {
        stringQuery += "&search=" + search
    }

    if (sort.length = 0) {
        stringQuery += "&sort=name"
    } else {
        stringQuery += "&sort=" + sort
    }

    window.location.replace("search?page=" + page + stringQuery)
    return false
}
