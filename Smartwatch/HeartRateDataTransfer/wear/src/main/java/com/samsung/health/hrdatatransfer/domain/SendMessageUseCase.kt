package com.samsung.health.hrdatatransfer.domain

import android.util.Log
import com.samsung.health.data.TrackedData
import com.samsung.health.hrdatatransfer.data.MessageRepository
import com.samsung.health.hrdatatransfer.data.TrackingRepository
import com.samsung.health.hrdatatransfer.data.model.User
import com.samsung.health.hrdatatransfer.data.remote.ApiService
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import retrofit2.Response
import java.time.LocalDate
import javax.inject.Inject

private const val TAG = "SendMessageUseCase"
private const val MESSAGE_PATH = "/msg"

class SendMessageUseCase @Inject constructor(
    private val messageRepository: MessageRepository,
    private val trackingRepository: TrackingRepository,
    private val getCapableNodes: GetCapableNodes,
    private val apiService: ApiService // Adicione a injeção do ApiService
) {
    suspend operator fun invoke(): Boolean {
        val nodes = getCapableNodes()

        return if (nodes.isNotEmpty()) {
            val node = nodes.first()
            val message = encodeMessage(trackingRepository.getValidHrData())
            messageRepository.sendMessage(message, node, MESSAGE_PATH)

            // Obtenha os dados de ibi e Hr do TrackedData
            val trackedData = trackingRepository.getValidHrData().firstOrNull()
            trackedData?.let {
                val user = User(
                    id_patient = "Sara",
                    dateTime = LocalDate.now().toString(), // Convertido para String
                    ibi = it.ibi
                )
                sendUserToApi(user)
            }

            true
        } else {
            Log.i(TAG, "Ain't no nodes around")
            false
        }
    }

    // Ajuste para usar corrotinas em vez de callback
    private suspend fun sendUserToApi(user: User) {
        try {
            val response: Response<Void> = apiService.createUser(user)  // Agora, a chamada retorna Response<Void>
            if (response.isSuccessful) {
                Log.i(TAG, "User successfully sent to API")
            } else {
                Log.e(TAG, "Failed to send user: ${response.code()}")
            }
        } catch (t: Throwable) {
            Log.e(TAG, "Error sending user to API: ${t.message}")
        }
    }

    private fun encodeMessage(trackedData: ArrayList<TrackedData>): String {
        return Json.encodeToString(trackedData)
    }
}
