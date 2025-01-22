package com.samsung.health.hrdatatransfer.di

import com.samsung.health.hrdatatransfer.data.remote.ApiService
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent

@Module
@InstallIn(SingletonComponent::class)  // Torna o módulo disponível em toda a aplicação
object NetworkModule {

    // Fornece a instância do Retrofit
    @Provides
    fun provideRetrofit(): Retrofit {
        return Retrofit.Builder()
            .baseUrl("https://10.224.1.127")  // Substitua pela URL do seu servidor
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    // Fornece a instância do ApiService
    @Provides
    fun provideApiService(retrofit: Retrofit): ApiService {
        return retrofit.create(ApiService::class.java)
    }
}