class ApiService {
    static async getProtectionZones() {
        try {
            const response = await fetch(`/api/protection_zones_geom/?is_show`)
            return await response.json()
        } catch (error) {
            console.error('Ошибка при получении охранных зон:', error)
        }
    }

    static async getProtectedObjects() {
        try {
            const response = await fetch(`/api/protected_objects_geom/`)
            return await response.json()
        } catch (error) {
            console.error('Ошибка при получении охраняемых объектов:', error)
        }
    }

    static async getOrtho() {
        try {
            const response = await fetch(`/api/geodata_files/?is_show`)
            return await response.json()
        } catch (error) {
            console.error('Ошибка при получении ортофотопланов:', error)
        }
    }

    // static async getZMR() {
    //     try {
    //         const response = await fetch(`/api/zmr_geom/`)
    //         return await response.json()
    //     } catch (error) {
    //         console.error('Ошибка при получении зон проектов:', error)
    //     }
    // }
    //
    // static async getOZ() {
    //     try {
    //         const response = await fetch(`/api/oz_geom/`)
    //         return await response.json()
    //     } catch (error) {
    //         console.error('Ошибка при получении охранной зоны:', error)
    //     }
    // }
}