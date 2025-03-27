document.addEventListener('DOMContentLoaded', function() {
    const addToCartButtons = document.querySelectorAll('.add-to-cart');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();  
            const productName = this.dataset.productName; 
            alert(`Adding ${productName} to your cart!`);
        });
    });
});