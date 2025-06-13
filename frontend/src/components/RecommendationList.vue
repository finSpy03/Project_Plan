<template>
  <div v-if="places.length" class="row row-cols-1 row-cols-md-2 g-4 mt-3">
    <div v-for="place in places" :key="place.Place_Id" class="col">
      <div class="card h-100 shadow-sm border-primary">
        <div class="card-body d-flex flex-column justify-content-between">
          <div>
            <h5 class="card-title text-primary fw-bold">{{ place.Place_Name }}</h5>
            <h6 class="card-subtitle mb-2 text-muted">
              📍 {{ place.City }} • {{ place.Category }}
            </h6>
            <p class="mb-2 text-warning fw-semibold">⭐ {{ place.Rating }}</p>
            <p class="card-text small" style="white-space: pre-line;">
              {{ place.Description }}
            </p>
            <a :href="place.google_maps" target="_blank" class="card-link text-decoration-none text-info">
              🌐 Lihat di Google Maps
            </a>
          </div>

          <div class="mt-3">
            <p class="fw-bold text-secondary mb-1">💬 Komentar Pengunjung:</p>
            <ul v-if="Array.isArray(place.comment)" class="list-group list-group-flush">
              <li v-for="(komentar, index) in place.comment" :key="index" class="list-group-item small">
                {{ komentar }}
              </li>
            </ul>
            <p v-else class="text-muted fst-italic small mt-1">
              🔎 {{ place.comment }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
  <p v-else class="text-center text-muted mt-4">Tidak ada hasil ditemukan.</p>
</template>

<script>
export default {
  props: ['places']
}
</script>
