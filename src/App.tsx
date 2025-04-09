import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

interface Sentence {
  text: string
  tagged: string | null
}

var data: Sentence[] = [
  {
    text: "שָׁלוֹם וּבְרָכָה! מָה שְׁלוֹמְכֶם?",
    tagged: null,
  },
  {
    text: "הִנֵּה הַמִּשְׁפָּט הָרִאשׁוֹן שֶׁאֲנִי הוֹלֵךְ לְתַיֵּג",
    tagged: null
  }
]

function App() {

  const [sentence, setSentence] = useState<Sentence>()
  const [countOf, setCountOf] = useState({ total: 10, count: 0 })

  useEffect(() => {
    setSentence(data[0])
  }, [])

  return (
    <>
      <div className='w-[100vw] flex flex-col dark:bg-gray-900 pb-10 pt-5 overflow-hidden' dir='rtl'>
        <h1 className='text-center text-2xl opacity-80 mb-5 text-blue-300'>מישקל - תיוג המונים</h1>
        <div className='text-center text-lg font-medium'>
          תויגו {countOf.count} משפטים מתוך ({countOf.total})
        </div>
        {
          sentence && (
            <>
              <textarea onChange={e => { }} className=' p-2.5 reseize rounded-lg mb-5 mt-10 textarea textarea-primary focus:outline-none outline-none border-gray-700 focus:border-gray-700 text-[36px] w-[80%] max-w-[800px] h-[200px] self-center' value={sentence.text} />
              <div className='flex flex-row m-auto'>
                <button className='btn btn-success btn-lg mb-5 bg-blue-300 text-white'>מוכן 🤗</button>
                <button className='btn btn-ghost btn-lg mb-5'>דלג</button>
              </div>
              <div className='flex flex-col items-center justify-center gap-3'>
                <div className='flex gap-2 m-auto text-center'>
                  הטמעה = <kbd className="kbd kbd-lg">1</kbd>
                  שווא נע = <kbd className="kbd kbd-lg">2</kbd>
                  איפוס = <kbd className="kbd kbd-lg">3</kbd>

                </div>
                <div className='flex gap-2 m-auto text-center'>
                  מוכן = <kbd className="kbd kbd-lg bg-green-700 text-white">Enter</kbd>
                  דלג = <kbd className="kbd kbd-lg bg-red-700 text-white">Esc</kbd>
                </div>
              </div>


              <span className='text-center mt-10'>תודה לכל המתייגים ❤️</span>
            </>
          )
        }
      </div>
    </>
  )
}

export default App
