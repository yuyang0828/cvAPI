# cvAPI

cv api version 1

## getObjectsThenLabel:
Input: one image (with multiple objects)

Output: 
{
objectNum:, 
objectList:[
{name:[], location:[]}
]
}


## getDetail
input: one image (with one object)

output:
{
objectLabel:[],
objectLogo:[],
objectText[],
objectColor:[
	{‘colorName’:,
	‘rgb’:[]
}
]
}
