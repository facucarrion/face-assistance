import { jwtVerify } from 'jose'

const token_secret = import.meta.env.TOKEN_SECRET ?? ''

export async function verifyJwt() {
  const token = localStorage.getItem('user')

  if (!token) return false

  try {
    const { payload } = await jwtVerify(
      token,
      new TextEncoder().encode(token_secret)
    )

    if (payload) {
      return true
    }

    return false
  } catch (error) {
    console.error(error)
    return false
  }
}
