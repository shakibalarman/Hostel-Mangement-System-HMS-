import axios, { AxiosError, type InternalAxiosRequestConfig } from 'axios'
import type { ApiErrorShape } from '../types'

const TOKEN_KEY = 'hms_token'

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token: string | null) {
  if (token) {
    localStorage.setItem(TOKEN_KEY, token)
  } else {
    localStorage.removeItem(TOKEN_KEY)
  }
}

export const api = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error: AxiosError<{ error?: ApiErrorShape; detail?: unknown }>) => {
    if (error.response?.status === 401) {
      setToken(null)
      if (window.location.pathname !== '/login') {
        window.location.assign('/login')
      }
    }
    return Promise.reject(normalizeError(error))
  },
)

export function normalizeError(
  error: AxiosError<{ error?: ApiErrorShape; detail?: unknown }>,
): ApiErrorShape {
  if (error.response?.data?.error) {
    return error.response.data.error
  }
  if (error.response?.data?.detail) {
    const detail = error.response.data.detail
    return {
      code: 'http_error',
      message: typeof detail === 'string' ? detail : 'Request failed',
    }
  }
  return {
    code: 'network_error',
    message: error.message || 'Network error. Please try again.',
  }
}
