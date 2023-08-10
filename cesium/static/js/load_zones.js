class ApiService {
    static async getZMR() {
        try {
            const response = await fetch(`/api/zmr_geometries/`)
            return await response.json()
        } catch (error) {
            console.error('Ошибка при получении зон проектов:', error)
        }
    }
}