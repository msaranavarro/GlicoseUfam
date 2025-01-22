package com.samsung.health.hrdatatransfer.data.model

data class User(
    val id_patient: String,
    val dateTime: String,
    val ibi: ArrayList<Int>
)
