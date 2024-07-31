document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const locationFields = document.getElementById('location-fields');
    
    function addFields() {
        locationFields.innerHTML = ''; 
        const trees = form.querySelectorAll('input[name="trees"]:checked');
        
        
        trees.forEach(tree => {
            const treeId = tree.value;
            //Get the text inside label tag
            const treeLabel = tree.nextSibling.textContent.trim();
            
            // Latitude field
            const latDiv = document.createElement('div');
            latDiv.className = 'form-group';
            latDiv.innerHTML = `
                <label for="latitude_${treeId}">Latitude for ${treeLabel}:</label>
                <input type="text" name="latitude_${treeId}" id="latitude_${treeId}" class="form-control" placeholder="Enter latitude">
            `;
            locationFields.appendChild(latDiv);
            
            // Longitude field
            const lonDiv = document.createElement('div');
            lonDiv.className = 'form-group';
            lonDiv.innerHTML = `
                <label for="longitude_${treeId}">Longitude for ${treeLabel}:</label>
                <input type="text" name="longitude_${treeId}" id="longitude_${treeId}" class="form-control" placeholder="Enter longitude">
            `;
            locationFields.appendChild(lonDiv);
        });
    }
    
    form.querySelectorAll('input[name="trees"]').forEach(input => {
        input.addEventListener('change', addFields);
    });
});