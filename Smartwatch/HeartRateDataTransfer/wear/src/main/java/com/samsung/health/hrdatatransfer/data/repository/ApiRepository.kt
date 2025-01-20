package com.samsung.health.hrdatatransfer.data.repository

import com.samsung.health.hrdatatransfer.data.remote.ApiService
import com.samsung.health.hrdatatransfer.data.model.User
import javax.inject.Inject

class ApiRepository @Inject constructor(private val apiService: ApiService) {
    fun sendUserData(user: User) = apiService.createUser(user)
}
