$(document).ready(function () {
    console.log("✅ JavaScript Loaded!");

    // ✅ Open Modal Function (Using Vanilla JS & jQuery)
    function openModal(songId) {
        fetch(`/api/song/${songId}/`)
            .then(response => response.json())
            .then(song => {
                console.log("✅ Song Data:", song); // Debugging step

                // ✅ Fill modal with song details
                $("#modal-title").text(song.title);
                $("#modal-artist").text(song.artist.name);
                $("#modal-artist-photo").attr("src", song.artist.picture_url || "/static/default_artist.jpg");
                $("#modal-artist-link").attr("href", song.artist.link);
                $("#modal-artist-fans").text(song.artist.fans_count);
                $("#modal-album").text(song.album.title || "N/A");
                $("#modal-album-cover").attr("src", song.album.cover_url || "/static/default_album.jpg");
                $("#modal-release-date").text(song.album.release_date || "Unknown");
                $("#modal-duration").text(`${Math.floor(song.duration / 60)}m ${song.duration % 60}s`);

                // ✅ Handle playback URL (Hide if not available)
                if (song.preview_url) {
                    $("#modal-playback-btn").show().attr("href", song.preview_url);
                } else {
                    $("#modal-playback-btn").hide();
                }

                // ✅ Show the modal
                $("#song-modal").fadeIn();
            })
            .catch(error => console.error("❌ Error fetching song details:", error));
    }

    // ✅ Close Modal Function
    function closeModal() {
        $("#song-modal").fadeOut();
    }

    // ✅ Close modal when clicking outside
    $(document).on("click", function (event) {
        if ($(event.target).is("#song-modal")) {
            closeModal();
        }
    });

    // ✅ Live Search
    $("#searchQuery").on("input", function () {
        let query = $(this).val().trim();
        let searchResults = $("#search-results");

        if (query.length > 1) {
            fetch(`/api/search?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    searchResults.empty();

                    if (data.songs.length > 0) {
                        searchResults.append(`<p class="px-4 py-2 text-gray-400 text-sm">🎵 Songs</p>`);
                        data.songs.slice(0, 5).forEach(song => {
                            searchResults.append(`<div class="search-item" onclick="openModal(${song.id})">
                                <img src="${song.cover_url || '/static/default_album.jpg'}">
                                <span>${song.title} 🎤 <span class="text-blue-400">${song.artist}</span></span>
                            </div>`);
                        });
                    }

                    if (data.albums.length > 0) {
                        searchResults.append(`<p class="px-4 py-2 text-gray-400 text-sm">📀 Albums</p>`);
                        data.albums.slice(0, 5).forEach(album => {
                            searchResults.append(`<div class="search-item">
                                <img src="${album.cover_url || '/static/default_album.jpg'}">
                                <span>${album.title} 🎤 <span class="text-blue-400">${album.artist}</span></span>
                            </div>`);
                        });
                    }

                    if (data.artists.length > 0) {
                        searchResults.append(`<p class="px-4 py-2 text-gray-400 text-sm">👤 Artists</p>`);
                        data.artists.slice(0, 5).forEach(artist => {
                            searchResults.append(`<div class="search-item">
                                <img src="${artist.cover_url || '/static/default_artist.jpg'}">
                                <span>${artist.name}</span>
                            </div>`);
                        });
                    }

                    // ✅ Add "View More Results" Option
                    searchResults.append(`<div class="view-more" onclick="window.location.href='/search-results?q=${query}'">View More Results →</div>`);

                    searchResults.show();
                })
                .catch(error => console.error("❌ Error fetching search results:", error));
        } else {
            searchResults.hide();
        }
    });

    // ✅ Expose functions to global scope for event listeners
    window.openModal = openModal;
    window.closeModal = closeModal;
});
