import { atom } from 'nanostores'

export const userToken = atom<string | null>(localStorage.getItem('user'))