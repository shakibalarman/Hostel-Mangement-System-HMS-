import { api } from './client'
import type { AuthTokens, User } from '../types'

export async function login(username: string, password: string): Promise<AuthTokens> {
  const params = new URLSearchParams({ username, password })
  const { data } = await api.post<AuthTokens>('/auth/login', params, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  return data
}

export async function getCurrentUser(): Promise<User> {
  const { data } = await api.get<User>('/auth/me')
  return data
}
