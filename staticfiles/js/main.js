$(document).ready(function () {
    let searchInput = $("#searchQuery");
    let searchResults = $("#search-results");
    let clearSearchBtn = $("#clearSearch");

    // ✅ Live Search Functionality
    searchInput.on("input", function () {
        let query = $(this).val().trim();

        if (query.length > 1) {
            fetch(`/api/search?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    searchResults.empty().show(); // Clear previous results & show dropdown

                    if (data.songs.length > 0) {
                        searchResults.append(`<p class="px-4 py-2 text-gray-400 text-sm">🎵 Songs</p>`);
                        data.songs.slice(0, 5).forEach(song => {
                            searchResults.append(`
                                <div class="search-item flex items-center px-4 py-2 text-gray-300 hover:bg-gray-700 cursor-pointer"
                                     onclick="selectSearchItem(${song.id}, 'song')">
                                    <img src="${song.cover_url || '/static/default_album.jpg'}" class="w-10 h-10 rounded-md mr-4">
                                    <span>${song.title} 🎤 <span class="text-blue-400">${song.artist}</span></span>
                                </div>`);
                        });
                    }

                    if (data.albums.length > 0) {
                        searchResults.append(`<p class="px-4 py-2 text-gray-400 text-sm">📀 Albums</p>`);
                        data.albums.slice(0, 5).forEach(album => {
                            searchResults.append(`
                                <div class="search-item flex items-center px-4 py-2 text-gray-300 hover:bg-gray-700 cursor-pointer"
                                     onclick="selectSearchItem(${album.id}, 'album')">
                                    <img src="${album.cover_url || '/static/default_album.jpg'}" class="w-10 h-10 rounded-md mr-4">
                                    <span>${album.title} 🎤 <span class="text-blue-400">${album.artist}</span></span>
                                </div>`);
                        });
                    }

                    if (data.artists.length > 0) {
                        searchResults.append(`<p class="px-4 py-2 text-gray-400 text-sm">👤 Artists</p>`);
                        data.artists.slice(0, 5).forEach(artist => {
                            searchResults.append(`
                                <div class="search-item flex items-center px-4 py-2 text-gray-300 hover:bg-gray-700 cursor-pointer"
                                     onclick="selectSearchItem(${artist.id}, 'artist')">
                                    <img src="${artist.cover_url || '/static/default_artist.jpg'}" class="w-10 h-10 rounded-full mr-4">
                                    <span>${artist.name}</span>
                                </div>`);
                        });
                    }

                    searchResults.append(`<div class="view-more px-4 py-3 text-center text-blue-400 hover:text-blue-300 bg-gray-900 cursor-pointer"
                                          onclick="window.location.href='/search-results?q=${query}'">
                                          View More Results →
                                      </div>`);
                })
                .catch(error => console.error("❌ Error fetching search results:", error));

            clearSearchBtn.show(); // Show ❌ button when input is not empty
        } else {
            searchResults.hide();
            clearSearchBtn.hide();
        }
    });

    // ✅ Function to handle selection of a search item (Song, Album, Artist)
    function selectSearchItem(id, type) {
        searchResults.hide(); // Hide the dropdown after selection

        if (type === "song") {
            openModal(id); // Open song modal
        } else if (type === "album") {
            window.location.href = `/album/${id}`; // Redirect to album page
        } else if (type === "artist") {
            window.location.href = `/artist/${id}`; // Redirect to artist page
        }
    }

    // ✅ Hide Dropdown When Clicking Outside
    $(document).on("click", function (event) {
        if (!$(event.target).closest("#searchQuery, #search-results").length) {
            searchResults.hide();
        }
    });

    // ✅ Clear Search Button Click
    clearSearchBtn.on("click", function () {
        searchInput.val("").focus();
        searchResults.hide();
        $(this).hide();
    });

    // ✅ Expose function globally
    window.selectSearchItem = selectSearchItem;

    // ✅ Open Modal Function
    function openModal(songId) {
        fetch(`/api/song/${songId}/`)
            .then(response => response.json())
            .then(song => {
                console.log("✅ Song Data:", song); // Debugging

                // ✅ Fill modal details
                $("#modal-title").text(song.title);
                $("#modal-artist").text(song.artist.name);
                $("#modal-album").text(song.album.title);
                $("#modal-release-date").text(song.album.release_date);
                $("#modal-duration").text(`${Math.floor(song.duration / 60)}m ${song.duration % 60}s`);

                // ✅ Album Cover
                $("#modal-album-cover").attr("src", song.album.cover_url || "/static/default_album.jpg");

                // ✅ Artist Photo
                $("#modal-artist-photo").attr("src", song.artist.picture_url || "/static/default_artist.jpg");

                // ✅ Show the modal
                $("#song-modal").removeClass("hidden");
            })
            .catch(error => console.error("❌ Error fetching song details:", error));
    }

    // ✅ Close Modal Function
    function closeModal() {
        $("#song-modal").addClass("hidden");
    }

    // ✅ Close modal when clicking outside
    $(document).on("click", function (event) {
        if ($(event.target).is("#song-modal")) {
            closeModal();
        }
    });

    // ✅ Expose functions globally for event listeners
    window.openModal = openModal;
    window.closeModal = closeModal;
});
