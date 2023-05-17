var baseUrl = "https://api.coinranking.com/v2/coins "
var proxyUrl = "https://cors-anywhere.herokuapp.com/"
var apiKey = "coinranking0497f3bb63d287f5203c68acaa24a00474291dc8ac384029"

fetch('./assets/crypto_data/data.json')
	.then((response) => response.json())
	.then((data) => {
		let preCoin = data
		fetch(`${baseUrl}`, {
			method: "GET",
			headers: {
				'Content-Type': 'application/json',
				'x-access-token': `${apiKey}`,
				'Access-Control-Allow-Origin': '*'
			}
		}).then((Response) => {
			if (Response.ok) {
				Response.json().then((json) => {
					console.log(json.data.coins)

					let coinsData = json.data.coins
					if (coinsData.length > 0) {
						var cryptoCoins = ""
					}

					//for loop starts
					preCoin.forEach((predicted) => {

						coinsData.forEach((coin) => {
							console.log(predicted.name)
							console.log(coin.symbol)

							if (predicted.name == coin.symbol) {
								let imgPath = "/img/" + (predicted.name) + ".png";

								cryptoCoins += `<div class="cryptoBox" id="coinsList">
						<div class="cryptoBox-header">
						  <img class="coinimg" src="${coin.iconUrl}" alt="bitconin">
						  <span class="left">${coin.name}</span>
						  <span class="right">$${Math.round(coin.price)}</span>
						</div>
						<div class="cryptoBox-middle">
						  <span class="left">Next Day Predicted Price</span>
						  <span class="right">$${Number(predicted.prediction).toFixed(2)}</span>
						</div>
						<div class="cryptoBox-footer">
						  <a href="${imgPath}">View More</a>
						</div>
					  </div>`
					  

							} else { console.log("coin name dose not match") }
						})
					})
					document.getElementById("coinsList").innerHTML = cryptoCoins


				})
			}
		}).catch((error) => {
			console.log(error)
		})
	});
