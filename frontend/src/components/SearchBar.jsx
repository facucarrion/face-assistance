import { useState } from "react"

const SearchBar = () => {
    const [search, setSearch] = useState("")

    const handleChange = event => {
        setSearch(event.target.value)
    }

    const handleSubmit = event => {
        event.preventDefault()
        const query = search.toLowerCase().replace(" ", "%20")
        location.href = `/search?q=${query}`
    }

    return(
        <form className='relative' onSubmit={handleSubmit}>
            <input
                id='search-input'
                type='text'
                placeholder='Buscar alumnos'
                className='bg-gray-200 text-black font-semibold px-4 py-2 rounded-lg hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500'
                onChange={handleChange}       
            />
            <button id='search-button' className='absolute right-0 top-0 mt-2 mr-2' type="sumbit">
                <img src='/search.svg' alt='Buscar' className='h-6 w-6' />
            </button>
        </form>
    )
}
export default SearchBar