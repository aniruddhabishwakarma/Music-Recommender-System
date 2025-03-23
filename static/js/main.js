$(document).ready(function () {
    let searchInput = $("#searchQuery");
    let searchResults = $("#search-results");
    let clearSearchBtn = $("#clearSearch");

    // ✅ Live Search
    searchInput.on("input", function () {
        let query = $(this).val().trim();

        if (query.length > 1) {
            fetch(`/api/search?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    searchResults.empty().show();

                    // 🎵 Songs
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

                    // 📀 Albums
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

                    // 👤 Artists
                    if (data.artists.length > 0) {
                        searchResults.append(`<p class="px-4 py-2 text-gray-400 text-sm">👤 Artists</p>`);
                        data.artists.slice(0, 5).forEach(artist => {
                            searchResults.append(`
                                <div class="search-item flex items-center px-4 py-2 text-gray-300 hover:bg-gray-700 cursor-pointer"
                                     onclick="selectSearchItem(${artist.id}, 'artist')">
                                    <img src="${artist.cover_url || '/static/music/images/images.png'}" class="w-10 h-10 rounded-full mr-4">
                                    <span>${artist.name}</span>
                                </div>`);
                        });
                    }

                    // View More
                    searchResults.append(`<div class="view-more px-4 py-3 text-center text-blue-400 hover:text-blue-300 bg-gray-900 cursor-pointer"
                        onclick="window.location.href='/search-results?q=${query}'">
                        View More Results →
                    </div>`);
                })
                .catch(error => console.error("❌ Error fetching search results:", error));

            clearSearchBtn.show();
        } else {
            searchResults.hide();
            clearSearchBtn.hide();
        }
    });

    // ✅ Handle selection
    function selectSearchItem(id, type) {
        searchResults.hide();

        if (type === "song") {
            fetch(`/api/song/${id}/`)
                .then(response => response.json())
                .then(song => {
                    console.log("🎵 Song from API:", song);
                    openModal(
                        song.song_id,
                        song.title,
                        song.artist.name,
                        song.album.cover_url || "/static/default_album.jpg",
                        song.minutes,
                        song.seconds,
                        song.artist.id,
                        song.artist.fans_count,
                        song.artist.picture_url || "/static/default_artist.jpg",
                        song.album.title,
                        song.album.release_date,
                        song.preview_url
                    );
                })
                .catch(error => console.error("❌ Error fetching song details:", error));
        } else if (type === "album") {
            window.location.href = `/album/${id}`;
        } else if (type === "artist") {
            window.location.href = `/artist/${id}`;
        }
    }

    // ✅ Click outside to close dropdown
    $(document).on("click", function (event) {
        if (!$(event.target).closest("#searchQuery, #search-results").length) {
            searchResults.hide();
        }
    });

    // ✅ Clear button
    clearSearchBtn.on("click", function () {
        searchInput.val("").focus();
        searchResults.hide();
        $(this).hide();
    });

    // ✅ Expose function globally
    window.selectSearchItem = selectSearchItem;
    window.closeModal = function () {
        $("#song-modal").addClass("hidden");
    };
});
