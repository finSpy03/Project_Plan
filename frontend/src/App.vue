<template>
  <div class="container py-5">
    <div class="text-center mb-4">
      <h1 class="fw-bold display-6 text-primary">🌍 Sistem Rekomendasi Wisata</h1>
      <p class="text-muted fs-6">Temukan destinasi terbaik berdasarkan lokasi atau kata kunci</p>
    </div>

    <!-- Kategori filter -->
    <div class="mb-4 d-flex flex-wrap gap-2 justify-content-center">
      <button
        v-for="k in kategoriList"
        :key="k"
        @click="setKategori(k)"
        :class="['btn btn-sm', kategoriAktif === k ? 'btn-primary' : 'btn-outline-primary']"
      >
        {{ k }}
      </button>
    </div>

    <InputForm @submit="fetchRecommendations" />

    <div v-if="isLoading" class="text-center text-secondary mt-3">🔄 Memuat rekomendasi...</div>
    <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>

    <RecommendationList :places="recommendedPlaces" />
  </div>
</template>

<script>
import InputForm from './components/InputForm.vue'
import RecommendationList from './components/RecommendationList.vue'

export default {
  components: { InputForm, RecommendationList },
  data() {
    return {
      recommendedPlaces: [],
      isLoading: false,
      errorMessage: '',
      kategoriList: [
        'Semua',
        'Tempat Ibadah',
        'Cagar Alam',
        'Budaya',
        'Bahari',
        'Pusat Perbelanjaan'
      ],
      kategoriAktif: 'Semua',
      lastKeyword: ''
    }
  },
  methods: {
    setKategori(kat) {
      this.kategoriAktif = kat
      if (this.lastKeyword) {
        this.fetchRecommendations(this.lastKeyword)
      }
    },
    async fetchRecommendations(keyword) {
      this.isLoading = true
      this.errorMessage = ''
      this.recommendedPlaces = []
      this.lastKeyword = keyword
      try {
        const params = new URLSearchParams()
        params.append('q', keyword.trim())
        if (this.kategoriAktif !== 'Semua') {
          params.append('category', this.kategoriAktif)
        }
        const res = await fetch(`https://silverBullet00-wisata-backend.hf.space/recommend/location?${params.toString()}`)
        if (!res.ok) throw new Error('Respon tidak OK')
        const data = await res.json()
        this.recommendedPlaces = data
        this.errorMessage = ''
      } catch (err) {
        console.error('Gagal mengambil rekomendasi:', err)
        this.errorMessage = 'Gagal mengambil data. Coba lagi.'
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>
