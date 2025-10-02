// script.js
document.addEventListener('DOMContentLoaded', function() {
    // Éléments du DOM
    const productForm = document.getElementById('product-form');
    const productImage = document.getElementById('product-image');
    const imagePreview = document.getElementById('image-preview');
    const productsContainer = document.getElementById('products-container');
    const modal = document.getElementById('confirmation-modal');
    const closeModal = document.querySelector('.close');
    const cancelBtn = document.querySelector('.cancel-btn');
    const confirmBtn = document.querySelector('.confirm-btn');
    
    let products = [];
    let productToDelete = null;
    
    // Prévisualisation de l'image
    productImage.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                imagePreview.innerHTML = `<img src="${e.target.result}" alt="Aperçu de l'image">`;
                imagePreview.style.display = 'block';
            }
            
            reader.readAsDataURL(file);
        }
    });
    
    // Soumission du formulaire
    productForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const name = document.getElementById('product-name').value;
        const description = document.getElementById('product-description').value;
        const price = document.getElementById('product-price').value;
        const imageFile = productImage.files[0];
        
        if (imageFile) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                const newProduct = {
                    id: Date.now(),
                    name,
                    description,
                    price,
                    image: e.target.result
                };
                
                products.push(newProduct);
                renderProducts();
                productForm.reset();
                imagePreview.style.display = 'none';
                imagePreview.innerHTML = '';
                
                alert('Produit ajouté avec succès!');
            };
            
            reader.readAsDataURL(imageFile);
        }
    });
    
    // Rendu des produits
    function renderProducts() {
        productsContainer.innerHTML = '';
        
        products.forEach(product => {
            const productCard = document.createElement('div');
            productCard.className = 'product-card';
            productCard.innerHTML = `
                <div class="product-image">
                    <img src="${product.image}" alt="${product.name}">
                </div>
                <div class="product-info">
                    <h4 class="product-name">${product.name}</h4>
                    <p class="product-description">${product.description}</p>
                    <div class="product-price">${product.price} FCFA</div>
                    <div class="product-actions">
                        <button class="edit-btn" data-id="${product.id}">
                            <i class="fas fa-edit"></i> Modifier
                        </button>
                        <button class="delete-btn" data-id="${product.id}">
                            <i class="fas fa-trash"></i> Supprimer
                        </button>
                    </div>
                </div>
            `;
            
            productsContainer.appendChild(productCard);
        });
        
        // Ajout des écouteurs d'événements pour les boutons
        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const id = parseInt(this.getAttribute('data-id'));
                showDeleteModal(id);
            });
        });
        
        document.querySelectorAll('.edit-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const id = parseInt(this.getAttribute('data-id'));
                editProduct(id);
            });
        });
    }
    
    // Afficher la modal de confirmation de suppression
    function showDeleteModal(id) {
        productToDelete = id;
        modal.style.display = 'flex';
    }
    
    // Fermer la modal
    closeModal.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    
    cancelBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    
    // Confirmer la suppression
    confirmBtn.addEventListener('click', function() {
        if (productToDelete) {
            products = products.filter(product => product.id !== productToDelete);
            renderProducts();
            modal.style.display = 'none';
            productToDelete = null;
        }
    });
    
    // Édition d'un produit
    function editProduct(id) {
        const product = products.find(p => p.id === id);
        
        if (product) {
            document.getElementById('product-name').value = product.name;
            document.getElementById('product-description').value = product.description;
            document.getElementById('product-price').value = product.price;
            
            // Pour l'image, on ne peut pas définir la valeur d'un input file pour des raisons de sécurité
            // On peut afficher un aperçu et gérer l'édition différemment
            imagePreview.innerHTML = `<img src="${product.image}" alt="Aperçu de l'image">`;
            imagePreview.style.display = 'block';
            
            // Supprimer l'ancien produit
            products = products.filter(p => p.id !== id);
            
            // Faire défiler jusqu'au formulaire
            document.querySelector('.admin-panel').scrollIntoView({ behavior: 'smooth' });
        }
    }
    
    // Fermer la modal en cliquant à l'extérieur
    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    // Données initiales (pour la démonstration)
    const initialProducts = [
        {
            id: 1,
            name: "Bijoux en or",
            description: "Magnifique bijoux en or 24 carats, fabrication artisanale.",
            price: "1500",
            image: "images/OIP.webp"
        },
        {
            id: 2,
            name: "Collier argent",
            description: "Collier en argent avec pendentif, design élégant.",
            price: "1200",
            image: "images/OIP.webp"
        },
        {
            id: 3,
            name: "Bracelet perles",
            description: "Bracelet en perles naturelles, plusieurs coloris disponibles.",
            price: "1800",
            image: "images/OIP.webp"
        }
    ];
    
    products = [...initialProducts];
    renderProducts();
});