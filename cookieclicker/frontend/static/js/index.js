/**
* Класс, в котором хранятся данные игры пользователя и основные методы взаимодействия с этими данными.
* Пусть вас не смущает слово function в начале, в JS так можно определять классы.
*/
function GameSession() {
    this.coins = 0
    this.click_power = 1
    this.auto_click_power = 0
    this.next_level_price = 10

    /** Метод для инициализации данных. Данные подгружаются с бэкенда. */
    this.init = function() {
        getCore().then(core => {
            this.coins = core.coins
            this.click_power = core.click_power
            this.auto_click_power = core.auto_click_power
            this.next_level_price = core.next_level_price
            render()
        })
    }
    /** Метод для добавления монеток. */
    this.add_coins = function(coins) {
        this.coins += coins
        this.check_levelup()
        render()
    }
    /** Метод для добавления невероятной мощи. */
    this.add_power = function(power) {
        this.click_power += power
        render()
    }
    /** Метод для добавления дружинника в отряд автоматизированных кликуш. */
    this.add_auto_power = function(power) {
        this.auto_click_power += power
        render()
    }
    /** Метод для проверки на повышения уровня. Отправка запроса на сохранение данных, если уровень повышен. */
    this.check_levelup = function() {
        if (this.coins >= this.next_level_price) {
            updateCoins(this.coins).then(core => {
                this.next_level_price = core.next_level_price
            })
        }
    }
}

let Game = new GameSession() // Экземпляр класса GameSession.

/** Функция обработки клика пользователя на какаши. */
function call_click() {
    const imgnode = document.getElementById('btn-img')
    click_animation(imgnode, 50)
    Game.add_coins(Game.click_power)
}

/** Функция для обновления количества монет, невероятной мощи и дружинных кликуш в HTML-элементах. */
function render() {
    const coinsNode = document.getElementById('coins')
    const clickNode = document.getElementById('click_power')
    const autoClickNode = document.getElementById('auto_click_power')
    coinsNode.innerHTML = Game.coins
    clickNode.innerHTML = Game.click_power
    autoClickNode.innerHTML = Game.auto_click_power
}

/** Функция для обновления буста на фронтике. */
function update_boost(boost) {
    const boost_node = document.getElementById(`boost_${boost.id}`)
    boost_node.querySelector('#boost_level').innerText = boost.level
    boost_node.querySelector('#boost_power').innerText = boost.power
    boost_node.querySelector('#boost_price').innerText = boost.price
}

/** Функция для добавления буста на фронтике. */
function add_boost(parent, boost) {
    const button = document.createElement('button')
    button.setAttribute('class', `boost_${boost.type}`)
    button.setAttribute('id', `boost_${boost.id}`)
    button.setAttribute('onclick', `buy_boost(${boost.id})`)
    button.innerHTML = `
        <p>lvl: <span id="boost_level">${boost.level}</span></p>
        <p>+<span id="boost_power">${boost.power}</span></p>
        <p><span id="boost_price">${boost.price}</span></p>
    `
    parent.appendChild(button)
}

/** Функция для анимации элемента, по которому происходит клик. */
function click_animation(node, time_ms) {
    css_time = `.0${time_ms}s`
    node.style.cssText = `transition: all ${css_time} linear; transform: scale(0.95);`
    setTimeout(function() {
        node.style.cssText = `transition: all ${css_time} linear; transform: scale(1);`
    }, time_ms)
}

/** Функция получения данных об игре пользователя с бэкенда. */
function getCore() {
    return fetch('/backend/core/', {
        method: 'GET'
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response)
    }).then(response => {
        return response.core
    }).catch(error => console.log(error))
}

/** Функция отправки данных о количестве монет пользователя на бэкенд. */
function updateCoins(current_coins) {
    const csrftoken = getCookie('csrftoken')
    return fetch('/backend/update_coins/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            current_coins: current_coins
        })
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response)
    }).then(response => {
        if (response.is_levelup) {
            get_boosts()
        }
        return response.core
    }).catch(error => console.log(error))
}

/** Функция получения имеющихся бустов пользователя с бэкенда. */
function get_boosts() {
    return fetch('/backend/boosts', {
        method: 'GET'
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response)
    }).then(boosts => {
        const panel = document.getElementById('boosts-holder')
        panel.innerHTML = ''
        boosts.forEach(boost => {
            add_boost(panel, boost)
        })
    }).catch(error => console.log(error))
}

/** Функция покупки буста. */
function buy_boost(boost_id) {
    const csrftoken = getCookie('csrftoken')
    return fetch(`/backend/boosts/${boost_id}/`, {
        method: 'PUT',
        headers: {
            "X-CSRFToken": csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            coins: Game.coins
        })
    }).then(response => {
        if (response.ok) return response.json()
        return Promise.reject(response)
    }).then(response => {
        if (response.error) return
        const old_boost_stats = response.old_boost_stats
        const new_boost_stats = response.new_boost_stats

        Game.add_coins(-old_boost_stats.price)
        if (old_boost_stats.type === 1) {
            Game.add_auto_power(old_boost_stats.power)
        } else {
            Game.add_power(old_boost_stats.power)
        }
        update_boost(new_boost_stats) // Обновляем буст на фронтике.
    }).catch(err => console.log(err))
}

/** Функция обработки автоматического клика. */
function setAutoClick() {
    setInterval(function() {
        /** Этот код срабатывает раз в секунду. */
        Game.add_coins(Game.auto_click_power)
    }, 1000)
}

/** Функция обработки автоматического сохранения (отправки данных о количестве монет пользователя на бэкенд). */
function setAutoSave() {
    setInterval(function() {
        /** Этот код срабатывает раз в минуту. */
        updateCoins(Game.coins)
    }, 60000)
}

/**
    Функция для получения кукесов.
    Она нужна для того, чтобы получить токен пользователя, который хранится в cookie.
    Токен пользователя, в свою очередь, нужен для того, чтобы система распознала, что запросы защищены.
    Без него POST и PUT запросы выполняться не будут, потому что так захотел Django.
*/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
* Эта функция автоматически вызывается сразу после загрузки страницы.
* В ней мы можем делать что угодно.
*/
window.onload = function () {
    Game.init() // Инициализация игры.
    setAutoClick() // Инициализация автоклика.
    setAutoSave() // Инициализация автосейва.
}