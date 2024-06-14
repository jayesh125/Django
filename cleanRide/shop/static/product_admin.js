// product_admin.js

document.addEventListener('DOMContentLoaded', function() {
    const categorySelect = document.querySelector('#id_category');
    const subCategorySelect = document.querySelector('#id_subcategory');

    categorySelect.addEventListener('change', function() {
        const categoryId = this.value;
        fetchSubcategories(categoryId);
    });

    function fetchSubcategories(categoryId) {
        fetch(`/get_subcategories/?category_id=${categoryId}`)
            .then(response => response.json())
            .then(data => {
                subCategorySelect.innerHTML = '';
                data.subcategories.forEach(subcategory => {
                    const option = document.createElement('option');
                    option.value = subcategory.id;
                    option.textContent = subcategory.name;
                    subCategorySelect.appendChild(option);
                });
            });
    }
});
