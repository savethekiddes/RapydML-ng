# RapydML XML/HTML Abstraction Markup Language

What is RapydML?
----------------
RapydML is a Pythonic abstraction for XML/HTML. The compiler generates HTML or HTML-like templates for Rails, Django, web2py or other frameworks (via templates) from indented, Python-like syntax. RapydML can also compile into arbitrary XML-like markup (such as SVG) based on a set of rules from user-defined template. These templates can have varying level of restrictions (compare the included lax HTML template against strict HTML5, for example).

Note that RapydML is still in beta. Some features and syntax could change in the future. Feel free to contact us with your own suggestions, if you have any.

Installation
------------
You can download RapydML from Github by clicking [here](https://github.com/savethekiddes/RapydML-ng/archive/refs/heads/main.zip) and extract it to a directory on your home computer. Alternatively, you can download it from our repository using the terminal directly:

	git clone https://github.com/savethekiddes/RapydML-ng.git

Afterwards, navigate to the root directory, and run the following commands to perform the installation:

    pip install subprocess --user
	python setup.py install

This will allow you to compile `.pyml` projects.


Compilation
-----------
Using RapydML is pretty straightforward. Assuming you have added an alias for it (or placed it in one of the directories covered by the system path), you can run it as follows:

	python rapydml.py <location of file>

RapydML also allows you to use alternative XML-like syntax. If you decide to do so, you can place your file in `markup` directory inside of RapydML and it will automatically be pulled into RapydML. You can then compile your file using a different markup:

	python rapydml.py --markupname <location of file>

RapydML already includes `HTML`, `HTML5`, and `ANY` markups you can use as examples. For more options and information, you can invoke rapydml's help:

	python rapydml.py -h


Getting Started
---------------
RapydML is pre-parser that allows you to write HTML (or any other XML-like markup) in more readable, Python-like format. The parser then generates HTML for you, automatically closing/aligning different HTML tags (it can even be told to avoid closing tags for certain elements - like !DOCTYPE). It's similar to SASS/SCSS, but for HTML (similar concept to HAML). Like SASS/SCSS/HAML, RapydML generates the page before it's deployed, and not dynamically as it's being served, saving you CPU cycles. Take a look at the following HTML, for example:

	<html>
		<head>
			<title>Welcome to my Web Page</title>
		</head>
		<body>
			<div id="title">
				<img src="banner.png" alt="My Banner" />
			</div>
			<div id="content">
				I haven't yet put anything on this page
			</div>
			<div id="copyright">
				Copyright 2012 by Me
			</div>
		</body>
	</html>

We can rewrite the above using RapydML as follows:

	html:
		head:
			title:
				"Welcome to my Web Page"
		body:
			div(id="title"):
				img(src="banner.png", alt="My Banner")
			div(id="content"):
				"I haven't yet put anything on this page"
			div(id="copyright"):
				"Copyright 2012 by Me"


Loops and Code Reuse
--------------------
We can pass in attributes as if they're arguments in a function call. We can already see that RapydML code is shorter and cleaner, but this becomes even more apparent in larger HTML files. Let us add a few images to our page to show that we support all major browsers, for example. We'll need to modify our content div as follows:

	<div id="content">
		I haven't yet put anything on this page
		<p>
			Compatible with all major browsers:
			<img src="Firefox.jpg" alt="Firefox" />
			<img src="Chrome.jpg" alt="Chrome" />
			<img src="IE.jpg" alt="IE" />
			<img src="Opera.jpg" alt="Opera" />
			<img src="Safari.jpg" alt="Safari" />
		</p>
	</div>

In RapydML we can accomplish the same thing with less repeated code using a loop:

	div(id="content"):
		"I haven't yet put anything on this page"
		p:
			"Compatible with all major browsers:"
			for $browser in [Firefox, Chrome, IE, Opera, Safari]:
				img(src="$browser.jpg", alt="$browser")

But what if our alt attributes don't happen to match our image names? That can be remedied as well, by grouping variables via sub-arrays:

	div(id="content"):
		"I haven't yet put anything on this page"
		p:
			"Compatible with all major browsers:"
			for $item in [[firefox, Firefox], [chrome, Chrome], [ie, Internet Explorer], [opera, Opera], [safari, Safari]]:
				img(src="$item[0].jpg", alt="$item[1]")


Variables and Sequences
-----------------------
Notice how we declare variables in RapydML. All variables must be preceeded by $, like in perl. While awkward at first, this actually allows us to more easily distinguish variables from HTML tags, and allows us better syntax highlighting of variables, something Python doesn't have. The assignment operator is := instead of the typical = sign. This is to avoid clashing with HTML's = sign if it happens to be part of the variable's value, as shown in example below:

	$src := src="smiley.gif", alt="A Smiley"
	for $i in [0:100]:
		img($src)
	
We don't need to quote whatever we're assigning to the variable, the leading/lagging whitespace will automatically get stripped, the whitespace in the middle will get preserved. Note the use of a shorthand to create an array of 101 consecutive integers. This shorthand works similar to Python's range() function. The first argument specifies the minimum, the second specifies the maximum (not maximum+1 like Python's range()), the third argument is optional and represents the step size. Here are some examples:

	[0:6]		-> [0,1,2,3,4,5,6]
	[1:8:2]		-> [1,3,5,7]
	[8:1:-1]	-> [8,7,6,5,4,3,2,1]
	[8:1]		-> []


Methods and HTML Chunks
-----------------------
If you find yourself reusing the same HTML in multiple places, but not in sequential order (preventing you from using a loop), you can define a method, which you can then invoke. A RapydML method is a chunk of HTML, which then gets plugged in every time the method call occurs. For example, here is how we could create a navigation menu, reusing the same button logic:

	def navbutton($text):
		div(class='nav-button'):
			img(src="$text.png", alt="Navigate to $text")
	
	div(id='nav-menu'):
		navbutton('Main')
		navbutton('Products')
		navbutton('Blog')
		navbutton('About')

There is another subtle, but extremely useful feature methods have. Method calls can have child elements. These children will get appended inside the last outer-level element declared inside the method. For example, if you're creating a page with multiple sections, and the content layout inside each section differs, you can do the following:

	def subsection($title):
		div(class="sub-section"):
			$title
		div(class="section-content")
	
	div(id="main"):
		subsection('Foo'):
			'This is the foo section, it only has text'
		subsection('Bar'):
			img(src="image.png")
			div:
				'Bar section has images, and sub-children'

Both, Foo and Bar, will append the children inside of the `section-content` div. This is a very powerful feature, allowing method content not only to get dumped inside of your page, but also wrap around other content in your page - similar to Python decorators. There is even more to this feature, which you can read about in the `Advanced Usage` section.


Math and String Manipulation
----------------------------
Like many other abstraction languages, RapydML can do a lot of the common logic for you. It has no concept of unit conversion like SASS, but it can easily handle many other things, like string manipulation, arithmetic, and mixing colors.


### Arithmetic and Colors

RapydML can handle basic arithmetic and color computations for you. For example, let's rewrite the above logic such that our navigation buttons start with dark blue and get brighter with each button:

	$color := #004
	def navbutton($text):
		div(class='nav-button', style="background: $color"):
			img(src="$text.png", alt="Navigate to $text")
	
	div(id='nav-menu'):
		for $i in ['Main', 'Products', 'Blog', 'About']:
			$color += #222
			navbutton($i)

Note that `$color` needs to be updated outside of a function. This is because RapydML shadows function variables, like Python. Moving `$color += #222` inside the function will update a local copy of `$color`, which gets discarded after the function terminates. RapydML is smart about colors. You can use the regular `#RRGGBB` format, shorthand `#RGB` form, or even html-accepted color name like `"Brown"`. When using html colors, it's important to use double-quotes around the color, otherwise it will be treated as a regular string. The color name itself, however, is not case sensitive, you can use "DarkBlue" or "darkblue", for example, or even "dArKbLuE". If no color with that name exists the string will be treated as a regular string. Mathematical computations are not limited to colors. You can also use them to compute dimensions of HTML elements, perform computations that get output on the page, or even concatenate strings:

	$height := 100
	$padding := 2
	$total := $height + $padding + 1	# border width of 1
	
	$name := 'smiley'
	$imgurl := 'static/images/' + $name + '.png'

You probably noticed the use of `+=`, which is a shorthand for incrementing. Here are a few other ones:

	$a += 2			# equivalent to: $a := $a + 2
	$a -= $b		# equivalent to: $a := $a - $b
	$a *= $b*2		# equivalent to: $a := $a * ($b*2)
	$a /= 5 + 2		# equivalent to: $a := $a / (5 + 2)

Lastly, there is a caveat about color arithmetic. While RapydML will limit min/max colors to be within allowed range, the color get converted to an integer when performing operations. This means that if you keep adding blue to a color that already reached maximum allowed amount of blue, RapydML will start adding green. This behavior could be modified in the future such that each channel is independent.


### Using Python Directly

RapydML will handle simple arithmetic and string concatenation for you, but what if you require more complex logic? RapydML has access to the full firepower of python (or at least its stdlib, you can't import Python modules). For example, let's say we wrote the following function to generate a button linking to one of the social media websites:

	def socialMedia($name):
		div(class="social-media"):
			a(href="www.$name.com"):
				img(src="$name.png" alt="$name")

The only problem is that the content of `$name` has to be in lowercase for the link to work. You could rename your PNG image to be in lowercase as well, but the `alt` text in all lowercase would look bad. Fortunately, RapydML can invoke Python's native logic if you use `python` prefix. Let's rewrite the above logic to capitalize the displayed text:

	def socialMedia($name):
		div(class="social-media"):
			a(href="www.$name.com"):
				img(src="$name.png" alt=python.str.capitalize("$name"))

Likewise, we could have instead used `python.str.lower()` if the `$name` was already capitalized before being passed into the function. RapydML compiler also auto-imports `math` module, allowing you to use logic like `python.math.sin(1)`. The `python.` prefix is not needed for Python methods that are nested inside other Python methods, like the following example:

	python.math.sin(min(1, 2, 3, 4))


Using Django, web2py, Rails, etc.
---------------------------------
RapydML easily extends to support any template engine your heart desires with just a few lines defining how to handle the given template. Take a look at the following example that adds support for Django's for loops:

	django = TemplateEngine('<%% %s %%>')
	django.for = create('for %s in %s:', 'endfor')

We now can invoke a Django for loop as follows:

	django.for(i, array):

Note that %s is used to specify the insertion of passed in arguments later, also note that %% is used to signify the actual percent sign character (like in Python, when using similar syntax). By passing a template to our TemplateEngine constructor, we tell it to wrap every call to django inside `<% %>` tags. Note also how a typical for loop gets declared. The fact that we called it `django.for` is just for convenience, we could have easily called it `django.loop` or any other keyword. What is important, however, is the arguments we pass to the creation method. The first argument represents the beginning of this block, the second represents the end of the block. In cases where the end block is irrelevant (such as `<%= item %>` tag), you can omit the second argument:

	django.out = create('= %s ')

But how does RapydML handle more complex template elements, such as an if/then/else block? With append() method, we can assign elif/else methods to the same consturct as an if statement. The following 3-liner adds support for if/then/else statements of any complexity:

	django.if = create('if %s:', 'endif')
	django.elif = django.if.append('elif %s:')
	django.else = django.if.append('else:')

Not bad, but what about more complex templating engines, such as web2py, that allow you to define functions inside of your view? Well, first of all, if you're defining functions inside of your view, you're probably doing something wrong (these should probably exist in the controller instead). But if you still desire to have them in your view, it's not that hard to accomplish. Let's take a look at the following chunk of code from Views chapter of the [web2py tutorial book](http://web2py.com/books/default/chapter/29/5):

	{{def itemize1(link): return LI(A(link, _href="http://" + link))}}
	<ul>
	{{=itemize1('www.google.com')}}
	</ul>

Remember the verbatim() method we showed you earlier for including arbitrary chunks of JavaScript and HTML inside of your page? This same method can be used here as well, and even happens to make the above code cleaner. In this case we will be using verbatim_line() method, which works just like the normal verbatim(), except it replaces all '\n' characters with spaces, which condenses your chunk of code into a single line:

	web2py.def = verbatim_line(web2py)

Now we can use the def method to define any methods we want inside our template. Let's rewrite the above chunk of code from web2py page:

	web2py.def:
		def itemize1(link):
			return LI(A(link, _href="http://" + link))

	ul:
		web2py.out(itemize1('www.google.com'))

While the code in this example isn't shorter than the original, you will probably agree that it is cleaner. That's fine, but if you had to include language template definitions in every HTML file you write, you would probably lose interest in RapydML pretty fast. To remedy this, you can use the `import` statement. Feel free to take all your Django/Web2py/Rails definitions and dump them into a separate file, naming it django.pyml, for example. Now add the following line to each one of your files that needs to use it:

	import django

Now you can even share your Django definitions with other developers. To keep things clean, you can even move template definitions to a separate directory, and reference them the same way you would in Python. If we decided to move our django.pyml template to views/templates directory, for example, we can then import it as follows:

	import views.templates.django

The notable difference here between Python and RapydML is the lack of namespaces. That means we would still reference the template engine by the same name as it's declared in the template file, rather than as we import it. So we would invoke the for loop as django.for(...) rather than views.templates.django.for(...). RapydML's import mechanism isn't as complex as Python's, we simply concatenate the contents of imported files into the main one, checking only that we don't import the same file multiple times.

To make it easier to write HTML, as well as create new templates, I have included templates for web2py, Django, and Rails, they're inside the `lib` directory. Feel free to use them to write your own web pages, as well as develop new templates for other engines. If you do plan to use a template engine, I suggest you also read the Advanced Usage section at the end. To add one of the included template engines to your project, simply add the following line at the top of your file:

	import lib.web2py


RapydML vs HAML
---------------
Admittedly, I started this as an afternoon hobby project, while being too naive to check that something like HAML already exists. After looking at HAML, however, I quickly realized that I like my solution much more than HAML. HAML takes the Rails approach, where it assumes things for you, and if those assumptions are correct, 'magic' happens. If they're not, you will spend a lot of time banging your head against a wall. HAML assumes that most tags will be DIVs, for example, replacing forgotten tags with DIVs for you. This assumption probably will not hold in the future. HTML5 already added multiple new tags (header, footer, article, nav, etc.) to reduce the number of DIVs needed on a page, and more tags will likely follow. HAML also also assumes that you will be using it with Rails to generate .erb files, you're out of luck if you use it with Django or Web2py. Like Rails, it's very good for doing things it was designed to do, but not something the developers didn't account for.

RapydML takes a more Pythonic approach, being simple, extensible, and explicit. You can extend it as you see fit, and it makes very few assumptions for you. You will also notice that RapydML code, while slightly longer, is much more readable than HAML, taking the Python approach here as well. You spend a lot more time looking at the code than writing it, so why make the code hard to read?

Additionally, RapydML is more powerful than HAML, even allowing the use of Python logic directly within the page. But perhaps the biggest advantage of RapydML is how customizable it is. By default, RapydML compiles into HTML and is very lax about HTML version, supporting any tags and attributes from HTML1.0 up until HTML5. It also includes a stricter HTML5 template in the `markup` directory, which you can use to ensure your web page is HTML5-compliant. The later template not only checks that your tags are valid, but also that you're using supported HTML5 attributes for them (for example, HTML5 dropped `bgcolor` attribute for `body` tag, and HTML5 template will tell you about that). Similarly, you can create new templates, specifying desired tag names as well as control how strict the template is (refer to `markup/html5` to understand template layout). Once done, just place the template into the `markup` directory, and it will automatically get pulled in by RapydML's compiler. Note that template's filename will become the name of the flag to invoke it, so if you add a file named `svg1`, you will need to invoke the compiler as follows to use it:

	rapydml --svg1 file.pyml


Advanced Usage
--------------
If you decide to use RapydML as the main tool for building your HTML, you might want to be familiar with some advanced features and tricks. If that's the case, this section is for you.


### Nesting Content Inside Methods

In the section titled `Methods and HTML Chunks`, we mentioned the ability to append content to a pre-declared method by indenting logic underneath the method call. There is even more to this feature, however. The indentation restriction is dictated by the content of the method, not the method call itself. This means that your indentation doesn't need to be correct relative to the method call, but rather the HTML chunk inside the method, and will get parsed relative to the method content as well. For example, imagine that we declared the following method:

	def content_box($title, $icon):
		div(class="content-box"):
			h1:
				$title
			div(class="content")
				img(src=$icon)
				div(class="content-text")

We now want to append content inside of the `content-text` div, but if we use the same way to append it as before, it will end up getting appended inside the main `content-box` div, as a sibling to `content` div and `h1` tag. Using the indentation trick we just discovered, however, we can control where to nest the content:

	content_box('Important Info', 'exclamation.png'):
				'This text will get appended to the inner-most div of content_box'

Likewise, if we used 2 indentations instead of 3, the content would get appended to the `content` div, right after the `content-text` div. This gives us great control of when and how our logic will get appended to the method, almost like using a multi-line variable. Another useful example is when you have a template method generating the parts of the page you plan to reuse:

	def template():
		html:
			head:
				...
			body:
				banner()
				div(id="content")

Without ability to control the indentation, you would be limited to placing your logic inside the outer-most tag, which is `html`. By using nested indentation, however, you can place content directly inside the `content` div, or just inside `body` itself (if it's a footer, for example).


### HTML Rendering Optimizations

If you're using web2py/Rails/Django or similar engine, you might have noticed that RapydML can handle some of the logic you previously relied on your templating engine for (things like combining content from multiple page templates/chunks, repeating portions of your HTML within the same page, etc.). You might be curious which solution is better. For that we'll need to understand what happens behind the scenes on your web server. Engines like web2py, Django, or Rails are useful for generating dynamic content that gets plugged into your HTML or even reducing the amount of repeated HTML markup between multiple web pages. They keep the code maintainable and ensure that you only need to make a change in one place to affect common logic on all of your your web pages.

Some of that niche, however, can be better addressed by RapydML. For example, you're probably familiar with the following line from Django (or its equivalent web2py or Rails):

	{% extends basic.html %}

For those unfamiliar with it, the above line includes HTML from basic.html inside of the current page. This is a useful technique to avoid unnecessary copies of HTML that's common to multiple pages (this includes navigation menus, website logo, etc.). The above logic, however, can also be substituted with RapydML's `import` statement, importing RapydML logic from another page. For example, I can create a template.pyml file, declararing a function for generating a chunk of reusable HTML inside of it, and then invoke that function in every place I want that HTML to appear. Which solution is better?

If you're an experienced web developer, you probably know that on most hosting services storage space (especially for text/html) is relatively cheap compared to bandwidth and CPU usage. The bandwidth requirements in this case are the same, since both, template engine and RapydML logic happens before the page is served to the client. The main difference is that by using `extends`, you force your template engine to dynamically generate that HTML content before serving it to the client (using up CPU cycles, smart engines will probably cache this data), while by using `import` you make your compiler generate that HTML once and serve it repeatedly to your clients (using up a bit more storage space, which is not even significant when comparing it to storage taken up by images and other multimedia files). As a rule of thumb, I recommend using RapydML's logic over Django/Rails/web2py unless it's something that requires information that will not be available until runtime (i.e. news that you retrieve from the database, interactive form that deals with user input). It's not too different from preferring CSS over JavaScript for styling that doesn't change dynamically.


### Writing DRY HTML/XML

RapydML does not evaluate the logic inside a method until it actually runs (gets invoked by logic not wrapped in a method). This means that you can call methods from other methods before they're declared. While subtle, this is a very useful feature. You can use this to take the importing idea presented in previous section a step further and do some really neat things with your website. For example, if you have a `template.pyml` file that defines `header_html()` and `footer_html()` methods (where header will take care of `<head>` declaration as well as the banner), your `index.pyml` will probably look like this:

	import template
	
	header_html():
		div(id="content"):
			'My page content'
			img(src="smiley.png")
		
		# resides inside header because header implements the <body> tag
		footer_html()

But you can do even better than that. Instead of implementing `header_html()` and `footer_html()`, let's write our `template.pyml` as follows:

	def page():
		html:
			head:
				title:
					'Welcome to my website'
			body:
				div(id="header")
					img(src="banner.png")
					
				div(id="content"):
					content()
				
				div(id="footer")
					'Copyright info'

If you're observant, you probably noticed the undefined `content()` method. That method will be defined by our `index.pyml` (and any other page based on this template), along with a call to `page()`, which will wrap the content inside of our template and generate the actual page:

	import template
	
	def content():
		'My page content'
		img(src="smiley.png")
	
	page()

The result is that our pages are very clean and all would-be repetitive content is in one place. In fact, pyjeon.com website is written using this technique.


### Nested Templates and Conditional Logic

RapydML does not have `if/else` statements, and for a good reason. RapydML is meant to make HTML cleaner, not more complicated. Adding more power than is needed to a language only makes it harder to read someone else's code. Since HTML is not meant to be dynamic, conditional logic would do more harm than good - especially when one developer does something fancy and another developer needs to make sense of it later.

However, there are valid cases when you need to generate pages with very similar layout, but not the same. Instead of having two very similar templates, you could use the latent method evaluation described in the previous section to create conditional logic within templates.

Similarly to calling an undeclared method inside another method, you can use an undeclared variable, as long as it gets defined by the time the method is called. Continuing from the example in previous section, let's say we have a `page()` method defined for drawing the generic page template. We now need to define a special set of pages based on that template, but sharing a sub-template as well. For example, let's say we're selling a product and the only things changing are its price, description, and name. We can create a new template called product_template:

	import template
	
	def content():
		h3:
			$name
		$description
		'Buy now for ' + $price
	
	def product_page():
		page()

Now for each of our products, we simply need to specify `$name`, `$description`, and `$price`, and call `product_page()` like so:

	import product_template
	
	$name := 'Coffee Mug'
	$description := 'A fancy coffee mug that keeps your coffee warm.'
	$price := '$8.99'
	
	product_page()

We can now invoke the same `product_page()` function, but the generated content will be unique for each product. We now have conditional templates without the messy `if/else` logic.


### Customizing Markup

RapydML is not limited to HTML. If you open up the `markup` directory, you will notice 3 files: `any`, `html`, and `html5`. `html` is the default markup RapydML assumes if you omit the markup modifier when compiling your `.pyml` file. This markup is designed to limit you to valid HTML tags, but does not enforce any attribute limitations or HTML versions. `html5` is much stricter, enforcing valid HTML5 tags as well as attributes. Finally, `any` is the most relaxed of the 3, allowing you to use any tag with any attributes. `any` markup assumes every tag which has not been explicitly defined as a method (via the use of `def` keyword inside of your `.pyml` file) to be a valid markup tag.

Using one of these as an example, you can create your own rules for any other *ML-like markup (SVG, XSLT, or XML that's custom to your project). The basic rules are very simple, but their combinations allow for very powerful customizations:

#### Rules

##### Line Format
Each line has to follow the following format (where whitespace can be one or more spaces or tabs, whitespace between attributes is not significant):

	<tagname>	allowedattr1, allowedattr2, ...

##### Example:

	<canvas>	height, width

##### Attribute Inheritance
Indentation is used to define child nodes, child nodes inherit allowed attributes from their parents

##### Example:

	<col>	span
		<colgroup>

##### Comments
`#` Marks beginning of a comment

##### Example:

	# this is a comment

##### Breaking Up Long Lines
When used at the end of the line, concatenates next line with current line, removing leading whitespace from next line

##### Example:

	<.>		attr1, attr2, attr3, \
			attr4, attr5

##### Internal/Meta Nodes
`<.>` Marks an internal node/tag, this node can't be used directly, but passes a set of usable attributes to its child tags, this should not be a leaf node.

##### Example:

	<.>	disabled, form, name
		<input>
		<button>

##### Wildcard Attributes
`*` If used instead of attributes, removes any argument restrictions from this tag

##### Example:

	<a>	*

##### Force Separate Close Tag
`+` Force this element to never use shorthand close: <div> allows <div />, <div>+ always forces <div></div>

##### Example:

	<canvas>+

##### Force No Close Tag
`-` Force this element to never use close tag, note that adding children under this element in your .pyml file will trigger an error

##### Example:

	<!DOCTYPE>-

##### Inheriting Attributes From Multiple Nodes
You can repeat the same tag multiple times, this is typically useful when it reuses same attributes as multiple other tags, yet those other tags don't share attributes. Note that when using + or - tag modifiers, the first occurence of the tag will be used for deciding the element/tag modifier. The rest will be ignored.

##### Example:

	<canvas>	height, width
		<input>	alt, src
	<button>	disabled, type, value
		<input>

##### Wildcard Elements/Tags
`<*>` A special tag, its presence means that omitted tags are allowed in pyml as well (and will automatically be inferred to use <tag></tag> format. Without this tag, RapydML will complain about any tags not specifically mentioned in the markup file.

##### Example:

	<*> attr1, attr2	# allows any element name as long as only attr1 or attr2 attributes are used

Note that wildcard tag is independent of wilcard attribute character. You can do each of the following for example:

	<*>		*		# places no restrictions on allowed elements or attributes 
					# (everything that wasn't explicitly declared as a method will 
					# be treated as an element tag)
	
	<foo>	*		# only allows `foo` element tag, but places no restrictions on 
					# usable attributes
	
	<*>		bar		# allows you to use any element tag name, but the only supported 
					# attribute for your elements is `bar`
	
	<foo>	bar		# only allows `foo` element tag, only allows `bar` attribute for it
	
	<*>				# places no restrictions on allowed elements, but does not allow 
					# any attributes (note that this only applies to elements that have
					# not been explicitly mentioned in the markup)

