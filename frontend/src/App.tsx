import { useState } from 'react'
import { PostList } from './components/PostList'
import { PostDetail } from './components/PostDetail'
import { CreatePost } from './components/CreatePost'
import { Login } from './components/Login'
import type { PostModel } from './api/types'
import './App.css'

type View = 'list' | 'detail' | 'create' | 'login'

function App() {
  const [view, setView] = useState<View>('list')
  const [selectedPost, setSelectedPost] = useState<PostModel | null>(null)
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'))
  const [userId, setUserId] = useState<number | null>(null)

  const handlePostClick = (post: PostModel) => {
    setSelectedPost(post)
    setView('detail')
  }

  const handleLoginSuccess = (accessToken: string, id: number) => {
    setToken(accessToken)
    setUserId(id)
    localStorage.setItem('token', accessToken)
    localStorage.setItem('userId', String(id))
    setView('list')
  }

  const handleLogout = () => {
    setToken(null)
    setUserId(null)
    localStorage.removeItem('token')
    localStorage.removeItem('userId')
  }

  return (
    <div className="app">
      <header>
        <h1>📰 Blog App</h1>
        <nav>
          <button onClick={() => setView('list')}>Posts</button>
          {token ? (
            <>
              <button onClick={() => setView('create')}>Create Post</button>
              <button onClick={handleLogout}>Logout</button>
            </>
          ) : (
            <button onClick={() => setView('login')}>Login</button>
          )}
        </nav>
      </header>

      <main>
        {view === 'list' && <PostList onPostClick={handlePostClick} />}
        {view === 'detail' && selectedPost && (
          <PostDetail post={selectedPost} onBack={() => setView('list')} />
        )}
        {view === 'create' && (
          <CreatePost onSuccess={() => setView('list')} token={token} userId={userId || 1} />
        )}
        {view === 'login' && <Login onLogin={handleLoginSuccess} />}
      </main>
    </div>
  )
}

export default App
