$(document).ready(function () {
// contact form handler
var contactForm = $(".contact-form")
var contactFormMethod = contactForm.attr("method")
var contactFormEndpoint = contactForm.attr("action")

var thisForm = $(this)
function displaySubmitting(submitBtn, defaultText, doSubmit){
    if (doSubmit){
        submitBtn.addClass("disabled")
        submitBtn.html("<i class='fa-duotone fa-solid fa-spinner'></i> sending.....")
    } else{
        submitBtn.removeClass("disabled")
        submitBtn.html(defaultText)
    }
    }
contactForm.submit(function(event) {
    event.preventDefault()
    var contactFormSubmitBtn = contactForm.find("[type='submit']")
    var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()
    var contactFormData =contactForm.serialize()
    displaySubmitting( contactFormSubmitBtn, "", true)
    $.ajax({
    method: contactFormMethod,
    url: contactFormEndpoint,
    data: contactFormData,
    success: function (data) {
        // Reset the form only if it's a valid HTML form element
        if (contactForm[0] instanceof HTMLFormElement) {
            contactForm[0].reset();
        } else {
            console.warn("contactForm[0] is not a valid form element.");
        }

        // Display success alert
        $.alert({
            title: "Success",
            content: data.message,
            theme: "modern",
        });
        setTimeout(function() {
            displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
        }, 800 )
    },
    error: function (error) {
        console.error("Error response:", error.responseJSON);
        const jsonData = error.responseJSON || {};
        let msg = "";

        // Build the error message
        $.each(jsonData, function (key, value) {
            if (Array.isArray(value) && value[0]?.message) {
                msg += `${key}: ${value[0].message}<br/>`;
            } else {
                msg += `${key}: ${value}<br/>`;
            }
        });

        // Display error alert
        $.alert({
            title: "Oops!",
            content: msg || "An unknown error occurred.",
            theme: "modern",
        });
        setTimeout(function() {
            displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
        }, 2000 )
    },

    // $.ajax({
    //     method: contactFormMethod,
    //     url: contactFormEndpoint,
    //     data: contactFormData,
    //     success: function(data){
    //         contactForm[0].reset()
    //         $.alert({
    //             title: "success",
    //             content: data.message,
    //             theme: 'modern',})
    //     },
    //     error: function(error){
    //         console.log(error.responseJSON)
    //         var jsonData = error.responseJSON
    //         var msg = ""
    //         $.each(jsonData, function(key, value){
    //             masg += key + ":" + value[0].message + "<br/>"
    //         })
    //         $.alert({
    //             title: "oops",
    //             content: msg,
    //             theme: 'modern', 
    //         })
    //     }
    })
    
})

// auto search 
var searchForm = $(".search-form")
var searchInput = searchForm.find("[name='q']")
var searchBtn = searchForm.find("[type='submit']")
var typingTimer;
var typingInterval = 500

searchInput.keyup(function(event){
    clearTimeout(typingTimer)
    typingTimer = setTimeout(performSearch, typingInterval)

})

searchInput.keydown(function(event){
    clearTimeout(typingTimer)
})

    function doSearch(){
        searchBtn.addClass("disabled")
        searchBtn.html("<i class='fa-duotone fa-solid fa-spinner'></i> Searching.....")

    }
    
    function performSearch(){
        doSearch()
        var query = searchInput.val()
        setTimeout(function(){
            window.location.href='/search/?q=' + query
        }, 1000)
        
    }

// cart add product
var productForm = $(".product-add-ajax")
productForm.submit(function(event) {
    event.preventDefault();
    console.log("form is not sending")
    var thisForm = $(this)
    //var actionEndpoint =thisForm.attr("action");
    var actionEndpoint = thisForm.attr("data-endpoint")
    var httpMethod = thisForm.attr("method");
    var formData = thisForm.serialize();
    
    $.ajax({
        url:actionEndpoint,
        method : httpMethod,
        data : formData,
        success : function(data){
            
            var submitSpan = thisForm.find(".submit-span")
            if (data.added){
                submitSpan.html("In cart<button type='submit' class='btn btn-link'>Remove?</button> ")
            }
            else {
                submitSpan.html("<button type='submit' class='btn btn-success'>Add to cart</button>")
            }
            var navbarCount = $(".navbar-cart-count")
            navbarCount.text(data.cartItemCount)
            var currentPath = window.location.href
            if (currentPath.indexOf("cart") != -1)
            refreshCart()

        },
        error: function(errorData){
            //$.alert("opps something is wrong")
            $.alert({
                title: "oops",
                content: 'sorry error occured while searching',
                theme: 'modern' 
            })
            console.log("error")
            console.log(errorData)

        }
    })
})
function refreshCart(){
    console.log("in current cart")
    var cartTable = $(".cart-table")
    var cartBody = cartTable.find(".cart-body")
    //cartBody.html("<h1>Changed</h1>")
    var productRows = cartBody.find(".cart-product")
    var currentUrl = window.location.href 

    var refreshCartUrl= '/api/cart'
    var refreshCartMethod = "GET";
    var data = {};
    $.ajax({
        url: refreshCartUrl,
        method: refreshCartMethod,
        data: data,
        success: function(data){
    
            var hiddenCartItemRemoveForm = $(".cart-item-remove-form")

            if (data.products.length > 0){
                productRows.html(" ")
                i = data.products.length
                $.each(data.products, function (index, value) {
                    var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                    newCartItemRemove.css("disply", "block")
                    newCartItemRemove.find(".cart-item-product-id").val(value.id)
                    cartBody.prepend("<tr><th scope=\"row\">" +  i + "</th><td><a href='" + value.url + "'>" + value.name + "</a>" + newCartItemRemove.html() + " </td>" + "<td>" + value.price +  "</td></tr>")
                    i --
                })
                
                cartBody.find(".cart-subtotal").text(data.subtotal)
                cartBody.find(".cart-total").text(data.total)
            } else {
                window.location.href = currentUrl
            }
            
        },
        error: function(errorData){
            $.alert({
                title: "oops",
                content: 'sorry error occured while searching',
                theme: 'modern' })
            console.log ("error")
            console.log(errorData)
        }
    })
}

})