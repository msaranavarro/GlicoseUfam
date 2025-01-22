package com.samsung.health.hrdatatransfer.data.remote

import com.samsung.health.hrdatatransfer.data.model.User
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.POST

interface ApiService {
    @POST("/post_patient_sensors.php")
    suspend fun createUser(@Body user: User): Response<Void>  // Alterado para suspend
}
