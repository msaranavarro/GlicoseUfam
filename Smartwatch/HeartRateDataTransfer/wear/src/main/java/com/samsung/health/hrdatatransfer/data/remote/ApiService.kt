package com.samsung.health.hrdatatransfer.data.remote

import com.samsung.health.hrdatatransfer.data.model.User
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.POST

interface ApiService {
    @POST("/api/insert")
    fun createUser(@Body user: User): Call<Void>
}
