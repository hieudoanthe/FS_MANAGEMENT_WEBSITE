
        function searchFunction() {
            
            var searchTerm = document.getElementById('searchInput').value.toLowerCase();
            var elementsToSearch = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, li');

            var searchResults = [];

            elementsToSearch.forEach(function(element) {
                // Neu chua phan tu tim kiem them vao ket qua 
                if (element.textContent.toLowerCase().includes(searchTerm)) {
                    searchResults.push(element.textContent);
                }
            });

            //hien thi
            displayResults(searchResults);
        }

        function displayResults(results) {
            var searchResultsList = document.getElementById('searchResults');
            searchResultsList.innerHTML = ''; // Xoa ket qua truoc

            // Tao cac phan tu danh sach moi cho ket qua 
            results.forEach(function(result) {
                var listItem = document.createElement('li');
                listItem.textContent = result;s
                searchResultsList.appendChild(listItem);
            });
        }
   
