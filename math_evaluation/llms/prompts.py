prompt_template = """You are a professional mathematical expert. Your task is to determine the answer type given the question statement. The possible answer types are listed as follows:

1. Real

\tDefinition: A real number is a number that can be used to measure a continuous one-dimensional quantity such as a distance, duration or temperature.

\tExample 1

Question: James creates a movie for $2000. Each DVD cost $6 to make. He sells it for 2.5 times that much. He sells 500 movies a day for 5 days a week. How much profit does he make in 20 weeks?
Answer: $448,000$
Analysis: Because the question asks about the profits, it means the answer $448,000$ should be a real number. So the comma is placed every third digit to the left of the decimal point and so is used in numbers with four or more digits. 
Type: Real

\tExample 2

Question: Solve the equation $x^2 - 2x + 1 = 0$.
Answer: $x = 1$
Analysis: The question requires the solution of an equation, and the answer "$x = 1$" is an equation that gives the specific real number solution for the variable $x$. So the answer is a real number.
Type: Real

2. Complex

\tDefinition: A complex number is a number that can be written in the form of $a + bi$, where $a$ and $b$ are real numbers and $i$ is the imaginary unit. 

\tExample 1

Question: Simplify $-3(1+4i)+i(-2-i)$.
Answer: $-2-14i$
Analysis: The answer is in the form $a + bi$ where $a=-2$ and $b=-14$. 
Type: Complex

\tExample 2

Question: Calculate $e^{{\\pi i}}$.
Answer: $-1$
Analysis: Even the question asks for the calculation on complex domain, the simplfied result is $-1$ reduces to a real number.
Type: Real

3. Set

\tDefinition: A set is a collection of different elements; these elements are typically mathematical objects of any kind.

\tExample 1

Question: Find all values of $k,$ for which there exists a nonzero vector $\\mathbf{{v}}$ such that\n\\[\\begin{{pmatrix}} 2 & -2 & 1 \\\\ 2 & -3 & 2 \\\\ -1 & 2 & 0 \\end{{pmatrix}} \\mathbf{{v}} = k \\mathbf{{v}}.\\]
Answer: $1,-3$
Analysis: The question requires to find all values of $k$, so the answer should be a set of $k$ values meeting the requirement.
Type: Set

\tExample 2

Question: Find all postive integers of $x$ such that $|x-1| < 1$. Express the results separated by comma(s).
Answer: 1
Analysis: The question requires to find positive integers of $x$ satisfying the inequality, but there is only one answer $1$. So the answer type is real.
Type: Real

4. Interval(s)

\tDefinition: An interval is a set of real numbers that lie between two fixed endpoints without any gaps. Intervals represent the intersection or union of several interval.

\tExample 1

Question: Solve the inequality $|x - 1| < 1$.
Answer: $(0, 2)$
Analysis: The question requires the solution of an inequality, so the answer $(0, 2)$ is an interval.
Type: Interval(s)

\tExample 2

Question: What is the domain of the real-valued function $f(x)=\\frac{{2x-7}}{{\\sqrt{{x^2-5x+6}}}}$?
Answer: $(-\\infty, 2) \\cup (3, \\infty)$
Analysis: The answer is the union of two intervals.
Type: Interval(s)

5. Vector

\tDefinition: A vector is a collection of ordered elements. These elements are typically mathematical objects of any kind. They can be equal but their order matters.

\tExample 1

Question: Find the interception of the line $y = -x + 2$ and the y-axis.
Answer: $(0, 2)$
Analysis: The interception of a line and the y-axis is a point, so the answer $(0, 2)$ represents the (x, y) coordinate and the order matters, which is a 2-dimensional vector.
Type: Vector

\tExample 2

Question: Find all positive integer values of $c$ such that the equation $x^2-7x+c=0$ only has roots that are real and rational. Express them in decreasing order, separated by commas.
Answer: $12, 10, 6$
Analysis: The question requires to find the roots and rational, but the answer is NOT the set type. The question also requires to express the answer in decreasing order and the set is unordered, so the correct type is vector.
Type: Vector

6. Matrix

\tDefinition: a rectangular array or table of numbers, symbols, or expressions, arranged in rows and columns, which is used to represent a mathematical object or a property of such an object.

\tExample 1

Question: A plane $P$ is parmeterized by\n\\[\\mathbf{{v}} = \\begin{{pmatrix}} 1 \\\\ 6 \\\\ 7 \\end{{pmatrix}} + t \\begin{{pmatrix}} 2 \\\\ -1 \\\\ -1 \\end{{pmatrix}} + s \\begin{{pmatrix}} 2 \\\\ -3 \\\\ -5 \\end{{pmatrix}},\\]and line $L$ is parameterized by\n\\[\\mathbf{{w}} = \\begin{{pmatrix}} 7 \\\\ 4 \\\\ 1 \\end{{pmatrix}} + u \\begin{{pmatrix}} 3 \\\\ 0 \\\\ -1 \\end{{pmatrix}}.\\]Find the intersection of plane $P$ and line $L.$
Answer: $\\begin{{pmatrix}} 1 \\\\ 4 \\\\ 3 \\end{{pmatrix}}$
Analysis: Even the answer is a matrix with shape $3 \\times 1$, which is a column vector, but the answer is in the form of $\\begin{{pmatrix}} ... \\end{{pmatrix}}$. We prefer the type Matrix.
Type: Matrix

\tExample 2

Question: For a 2 by 2 matrix $A$, can you find another matrix $B$, such that $AB = A$?
Answer: $[[0, 1], [1, 0]]$
Analysis: The answer is in the form of list of list, where each inner list has the same number of elements. We can conclude that the answer type is matrix.
Type: Matrix

7. Expression

\tDefinition: An expression is combination of symbols that is well-formed according to rules that depend on the context. There is usually at least one unknown variable, but no equal sign $=$ in the symbols.

\tExample 1

Question: Simplify $7a^3(3a^2 - a) - 8a(2a - 4)$.
Answer: $21a^5 - 7a^4 - 16a^2 + 32a$
Analysis: The answer is a polynomial with unknown variable $a$, so the type is expression.
Type: Expression

\tExample 2

Question: Calculate the area of a circle with radius $2$.
Answer: $4\\pi$
Analysis: The symbol $\\pi$ represents a mathematical constant, which is a real number. The type of answer $4\\pi$ is real.
Type: Real

8. Function

\tDefinition: A function from a set $X$ to a set $Y$ is an assignment of an element of $Y$ to each element of $X$. In our case, it is usually expressed as $f(x) = ...$ or $y = ...$.

\tExample 1

Question: A parabola has vertex $(4,2)$ and passes through $(2,0).$ Find the quadratic function that represents the parabola.
Answer: $f(x) = -\\frac{{1}}{{2}} x^2 + 4x - 6$
Analysis: The answer is a quadratic function which represents the parabola.
Type: Function

\tExample 2

Question: A parabola has vertex $(4,2)$ and passes through $(2,0).$ Find the equation of the parabola.
Answer: $y = -\\frac{{1}}{{2}} x^2 + 4x - 6$
Analysis: The answer is a quadratic function starts with $y = ...$ which represents the parabola. Either Function or Equation should be correct.
Type: Function

\tExample 3

Question: Find the maximum value of the quadratic function $y = -x^2 + 4x - 6$.
Answer: $y = -2$
Analysis: The question asks for calculating the maximum value of a function. The answer $y = -2$ represents the maxmium value $-2$, which is real number. 
Type: Real

9. Equation

\tDefinition: A equation states that two or more quantities are the same as one another, also called an equality or formula, in the form of $A = B$. In our case, at least one of $A$ and $B$ should have unknown variables. 

\tExample 1

Question: For a circle with its center as the origin, its curve also passes through $(-2, \\sqrt{{5}})$. What is its equation?
Answer: $x^2 + y^2 = 9$
Analysis: The answer is the circle equation $(x - h)^2 + (y - k)^2 = r^2$ where $h = k = 0$ and $r = 3$.
Type: Equation

\tExample 2

Question: A parabola has vertex $(4,2)$ and passes through $(2,0).$ Find the equation of the parabola.
Answer: $y = -\\frac{{1}}{{2}} x^2 + 4x - 6$
Analysis: The answer is a quadratic function starts with $y = ...$ which represents the parabola. Either Function and Equation should be correct.
Type: Equation

\tExample 3

Question: Find the tangent line of the circle $x^2 + y^2 = 4$ at point $(-2, 0)$.
Answer: $y = -2$
Analysis: The answer $y = -2$ represents the equation of the tangent line, NOT a real number.
Type: Equation

10. Inequality

\tDefinition: An inequality is a relation which makes a non-equal comparison between two numbers or other mathematical expressions.

\tExample 1

Question: The quadratic $f(x) = x^2 + bx + c$ satisfies $f(2 + t) = f(2 - t)$ for all real numbers $t.$ Find the relationship between the values of $f(1),$ $f(2),$ and $f(4)$.
Answer: $f(2) < f(1) < f(4)$
Anaylsis: The relation is represented in the form of inequality.
Type: Inequality

\tExample 2

Question: Solve the inequality $|x - 1| < 1$.
Answer: $0 < x < 2$
Analysis: The solution of the inequality is also in the form of an inequality.
Type: Inequality

11. Others

\tDefinition: If you can think the answer type is not one of above 10 types, select Others.

### Now! It's your turn. Remember to refer the definitions and examples, and follow the required template.

Question: the input question
Answer: the provided answer
Analysis: the analysis of type
Type: the type from the candidate types

### Begin!

Question: {question}
Answer: {ground_truth}
Analysis:"""


prompt_template_2 = """You are a professional mathematical expert. Your task is to determine the answer type given the question statement. The possible answer types are listed as follows:

1. Real

\tDefinition: A real number is a number that can be used to measure a continuous one-dimensional quantity such as a distance, duration or temperature.

2. Complex

\tDefinition: A complex number is a number that can be written in the form of $a + bi$, where $a$ and $b$ are real numbers and $i$ is the imaginary unit. 

3. Set

\tDefinition: A set is a collection of different elements; these elements are typically mathematical objects of any kind.

4. Interval(s)

\tDefinition: An interval is a set of real numbers that lie between two fixed endpoints without any gaps. Intervals represent the intersection or union of several interval.

5. Vector

\tDefinition: A vector is a collection of ordered elements. These elements are typically mathematical objects of any kind. They can be equal but their order matters.

6. Matrix

\tDefinition: a rectangular array or table of numbers, symbols, or expressions, arranged in rows and columns, which is used to represent a mathematical object or a property of such an object.

7. Expression

\tDefinition: An expression is combination of symbols that is well-formed according to rules that depend on the context. There is usually at least one unknown variable, but no equal sign $=$ in the symbols.

8. Function

\tDefinition: A function from a set $X$ to a set $Y$ is an assignment of an element of $Y$ to each element of $X$. In our case, it is usually expressed as $f(x) = ...$ or $y = ...$.

9. Equation

\tDefinition: A equation states that two or more quantities are the same as one another, also called an equality or formula, in the form of $A = B$. In our case, at least one of $A$ and $B$ should have unknown variables. 

10. Inequality

\tDefinition: An inequality is a relation which makes a non-equal comparison between two numbers or other mathematical expressions.

11. Others

\tDefinition: If you can think the answer type is not one of above 10 types, select Others.

### The following are several demonstration examples.

Question: James creates a movie for $2000. Each DVD cost $6 to make. He sells it for 2.5 times that much. He sells 500 movies a day for 5 days a week. How much profit does he make in 20 weeks?
Answer: $448,000$
Analysis: Because the question asks about the profits, it means the answer $448,000$ should be a real number. So the comma is placed every third digit to the left of the decimal point and so is used in numbers with four or more digits. 
Type: Real

Question: Solve the equation $x^2 - 2x + 1 = 0$.
Answer: $x = 1$
Analysis: The question requires the solution of an equation, and the answer "$x = 1$" is an equation that gives the specific real number solution for the variable $x$. So the answer is a real number.
Type: Real

Question: Simplify $-3(1+4i)+i(-2-i)$.
Answer: $-2-14i$
Analysis: The answer is in the form $a + bi$ where $a=-2$ and $b=-14$. 
Type: Complex

Question: Calculate $e^{{\\pi i}}$.
Answer: $-1$
Analysis: Even the question asks for the calculation on complex domain, the simplfied result is $-1$ reduces to a real number.
Type: Real

Question: Find all values of $k,$ for which there exists a nonzero vector $\\mathbf{{v}}$ such that\n\\[\\begin{{pmatrix}} 2 & -2 & 1 \\\\ 2 & -3 & 2 \\\\ -1 & 2 & 0 \\end{{pmatrix}} \\mathbf{{v}} = k \\mathbf{{v}}.\\]
Answer: $1,-3$
Analysis: The question requires to find all values of $k$, so the answer should be a set of $k$ values meeting the requirement.
Type: Set

Question: Find all postive integers of $x$ such that $|x-1| < 1$. Express the results separated by comma(s).
Answer: 1
Analysis: The question requires to find positive integers of $x$ satisfying the inequality, but there is only one answer $1$. So the answer type is real.
Type: Real

Question: Solve the inequality $|x - 1| < 1$.
Answer: $(0, 2)$
Analysis: The question requires the solution of an inequality, so the answer $(0, 2)$ is an interval.
Type: Interval(s)

Question: What is the domain of the real-valued function $f(x)=\\frac{{2x-7}}{{\\sqrt{{x^2-5x+6}}}}$?
Answer: $(-\\infty, 2) \\cup (3, \\infty)$
Analysis: The answer is the union of two intervals.
Type: Interval(s)

Question: Find the interception of the line $y = -x + 2$ and the y-axis.
Answer: $(0, 2)$
Analysis: The interception of a line and the y-axis is a point, so the answer $(0, 2)$ represents the (x, y) coordinate and the order matters, which is a 2-dimensional vector.
Type: Vector

Question: Find all positive integer values of $c$ such that the equation $x^2-7x+c=0$ only has roots that are real and rational. Express them in decreasing order, separated by commas.
Answer: $12, 10, 6$
Analysis: The question requires to find the roots and rational, but the answer is NOT the set type. The question also requires to express the answer in decreasing order and the set is unordered, so the correct type is vector.
Type: Vector

Question: A plane $P$ is parmeterized by\n\\[\\mathbf{{v}} = \\begin{{pmatrix}} 1 \\\\ 6 \\\\ 7 \\end{{pmatrix}} + t \\begin{{pmatrix}} 2 \\\\ -1 \\\\ -1 \\end{{pmatrix}} + s \\begin{{pmatrix}} 2 \\\\ -3 \\\\ -5 \\end{{pmatrix}},\\]and line $L$ is parameterized by\n\\[\\mathbf{{w}} = \\begin{{pmatrix}} 7 \\\\ 4 \\\\ 1 \\end{{pmatrix}} + u \\begin{{pmatrix}} 3 \\\\ 0 \\\\ -1 \\end{{pmatrix}}.\\]Find the intersection of plane $P$ and line $L.$
Answer: $\\begin{{pmatrix}} 1 \\\\ 4 \\\\ 3 \\end{{pmatrix}}$
Analysis: Even the answer is a matrix with shape $3 \\times 1$, which is a column vector, but the answer is in the form of $\\begin{{pmatrix}} ... \\end{{pmatrix}}$. We prefer the type Matrix.
Type: Matrix

Question: For a 2 by 2 matrix $A$, can you find another matrix $B$, such that $AB = A$?
Answer: $[[0, 1], [1, 0]]$
Analysis: The answer is in the form of list of list, where each inner list has the same number of elements. We can conclude that the answer type is matrix.
Type: Matrix

Question: Simplify $7a^3(3a^2 - a) - 8a(2a - 4)$.
Answer: $21a^5 - 7a^4 - 16a^2 + 32a$
Analysis: The answer is a polynomial with unknown variable $a$, so the type is expression.
Type: Expression

Question: Calculate the area of a circle with radius $2$.
Answer: $4\\pi$
Analysis: The symbol $\\pi$ represents a mathematical constant, which is a real number. The type of answer $4\\pi$ is real.
Type: Real

Question: A parabola has vertex $(4,2)$ and passes through $(2,0).$ Find the quadratic function that represents the parabola.
Answer: $f(x) = -\\frac{{1}}{{2}} x^2 + 4x - 6$
Analysis: The answer is a quadratic function which represents the parabola.
Type: Function

Question: A parabola has vertex $(4,2)$ and passes through $(2,0).$ Find the equation of the parabola.
Answer: $y = -\\frac{{1}}{{2}} x^2 + 4x - 6$
Analysis: The answer is a quadratic function starts with $y = ...$ which represents the parabola. Either Function or Equation should be correct.
Type: Function

Question: Find the maximum value of the quadratic function $y = -x^2 + 4x - 6$.
Answer: $y = -2$
Analysis: The question asks for calculating the maximum value of a function. The answer $y = -2$ represents the maxmium value $-2$, which is real number. 
Type: Real

Question: For a circle with its center as the origin, its curve also passes through $(-2, \\sqrt{{5}})$. What is its equation?
Answer: $x^2 + y^2 = 9$
Analysis: The answer is the circle equation $(x - h)^2 + (y - k)^2 = r^2$ where $h = k = 0$ and $r = 3$.
Type: Equation

Question: A parabola has vertex $(4,2)$ and passes through $(2,0).$ Find the equation of the parabola.
Answer: $y = -\\frac{{1}}{{2}} x^2 + 4x - 6$
Analysis: The answer is a quadratic function starts with $y = ...$ which represents the parabola. Either Function and Equation should be correct.
Type: Equation

Question: Find the tangent line of the circle $x^2 + y^2 = 4$ at point $(-2, 0)$.
Answer: $y = -2$
Analysis: The answer $y = -2$ represents the equation of the tangent line, NOT a real number.
Type: Equation

Question: The quadratic $f(x) = x^2 + bx + c$ satisfies $f(2 + t) = f(2 - t)$ for all real numbers $t.$ Find the relationship between the values of $f(1),$ $f(2),$ and $f(4)$.
Answer: $f(2) < f(1) < f(4)$
Anaylsis: The relation is represented in the form of inequality.
Type: Inequality

Question: Solve the inequality $|x - 1| < 1$.
Answer: $0 < x < 2$
Analysis: The solution of the inequality is also in the form of an inequality.
Type: Inequality

### Now! It's your turn. Remember to refer the definitions and examples, and follow the required template.

Question: the input question
Answer: the provided answer
Analysis: the analysis of type
Type: the type from the candidate types

### Begin!
Question: {question}
Answer: {ground_truth}
Analysis:"""

