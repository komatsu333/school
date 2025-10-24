class Pref:
	def __init__(self, id=0, kenmei="", kenchou="", jinkou=0, menseki=0, chihou="", jinkoumitudo=0) -> None:
		self._id = id
		self._kenmei = kenmei
		self._kenchou = kenchou
		self._jinkou = jinkou
		self._menseki = menseki
		self._chihou = chihou
		self._jinkoumitudo = jinkoumitudo

	def introduce(self) -> None:
		print(f"{self._id},{self._kenmei},{self._kenchou},{self._jinkou},{self._menseki},{self._chihou},{self._jinkoumitudo}")

	def __str__(self) -> str:
		return f"{self._id},{self._kenmei},{self._kenchou},{self._jinkou},{self._menseki},{self._chihou},{self._jinkoumitudo}"
#############################################
if __name__ == '__main__':
	p = Pref(1,"北海道","札幌市",5224614,83424.4,"北海道",62.6269)
	p.introduce()
