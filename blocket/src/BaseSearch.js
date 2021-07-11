
let convert = (obj, match=/[0-9\W]+(?= kr)/, replace=" ") => {
	/* converts the input object to int and replaces whitespace
	 * 
	 * Arguments:
	 * 	match: regex expression
	 *
	 * 	replace: string, to replace with none.
	 * */
	try {
		return (parseInt(
				obj
				.innerText.match(match)[0]
				.replace(replace, "")
		))
		// return (
		// 	obj
		// 	.innerText.match(match)[0]
		// 	.replace(replace, "")
	// )
	} catch {
		return "nan"
	}
}

let return_matrix = (dim1, dim2) => {
	let arr = new Array(dim1);
	for (let i=0; i<arr.length; i++){
		arr[i] = new Array(dim2)
	}
	return arr
}

class Blocket {
	constructor(){
	
	}
	
	search(){
		/* Performs basic search on the Blocket page to extract parts from each ad
		 * Arguments:
		 * 	None
		 *
		 * Keyword-arguments: 
		 * 	None
		 *
		 * Returns:
		 * 	None
		 * */
		let base = document.querySelectorAll('[class^=styled__Content-sc-]')

		// let base_price = document.querySelectorAll('[class^=styled__SalesInfo-sc-]');
		let data_matrix = return_matrix(base.length, 2);
		let price, mil;

		for (let i=0; i<base.length; i++){
			price = convert(base[i].children[3], /[0-9\W]+(?= kr)/, " ");
			mil = convert(base[i].children[2], /[0-9\W]+(?= mil)/, /\W/);
			
			if (price === "nan" | mil === "nan"){
				continue
			} else {
				// price
				data_matrix[i][0] = price;
	
				// mil
				data_matrix[i][1] = mil;
				
			}
		}
		data_matrix = data_matrix.filter((el)=>{
			return el[0] != null | el[1] != null
		})
		this.data_matrix = data_matrix;
		return data_matrix
	}

	
}

bl = new Blocket;
bl.search()

// document.querySelectorAll('[class^=styled__Content-sc-]').children[2], /[0-9\W]+(?= mil)/, " ")