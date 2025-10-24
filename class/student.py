class Student:

	def __init__(self,num,name,addr,age,highschool):
		self._num = num
		self._name = name
		self._addr = addr
		self._age = age
		self._highschool = highschool

	def introduce(self):
		print(f'私の名前は、{self._name}')
		print(f'    出身は、{self._addr}')
		print(f'    高校は、{self._highschool}')
		print(f'    年齢は、{self._age}')


if __name__ == '__main__':
	s = Student(1,'xxx','yyy',100,'zzz')
	s.introduce()
