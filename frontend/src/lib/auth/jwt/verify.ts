import { jwtVerify } from 'jose'

const token_secret = import.meta.env.PUBLIC_TOKEN_SECRET

export async function verifyJwt() {
  const token = localStorage.getItem('user')

  let status = false
  let payload = null

  if (!token) return { status, payload }

  try {
    const { payload } = await jwtVerify(
      token,
      new TextEncoder().encode(token_secret)
    )

    if (payload) {
      status = true
    }

    return { status, payload }
  } catch (error) {
    console.error(error)
    return { status, payload: null }
  }
}
