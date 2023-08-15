class ApiService {
    static async getZMR() {
        try {
            const response = await fetch(`/api/zmr_geom/`)
            return await response.json()
        } catch (error) {
            console.error('Ошибка при получении зон проектов:', error)
        }
    }

    static async getOZ() {
        try {
            const response = await fetch(`/api/oz_geom/`)
            return await response.json()
        } catch (error) {
            console.error('Ошибка при получении охранной зоны:', error)
        }
    }
}