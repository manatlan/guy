from dtags import ReactiveProp,Tag,DTag


def test_ReactiveProp():
    class Pojo: pass
    p=Pojo()
    p.a=12
    p.b=42

    a=ReactiveProp(p,"a")
    assert int(a)==12
    assert p.__dict__["a"]==12
    a.set(42)
    assert p.__dict__["a"]==42
    assert str(a)=="42"
    assert type(a+1) == ReactiveProp
    assert a+1 == 44

def test_Tag():
    assert str(Tag()) == '<div class="tag"></div>'
    assert str(Tag("hello")) == '<div class="tag">hello</div>'
    assert str(Tag("hello",klass="john doe")) == '<div class="john doe">hello</div>'
    assert str(Tag("hello",data_mining="hell")) == '<div data-mining="hell" class="tag">hello</div>'
    assert str(Tag("hello",42,klass="john doe")) == '<div class="john doe">hello 42</div>'
    assert str(Tag("hello",onclick='alert("bill & john")')) == '<div onclick="alert(&quot;bill &amp; john&quot;)" class="tag">hello</div>'

def test_Tag_id():
    t=Tag()
    t.id="nope"
    assert str(t) == '<div class="tag" id="nope"></div>'


def test_Tag_class():
    class Nope(Tag): pass
    assert str(Nope()) == '<div class="nope"></div>'
    assert str(Nope("hello")) == '<div class="nope">hello</div>'
    assert str(Nope("hello", klass='other') ) == '<div class="other">hello</div>'

    class Nope(Tag):
        klass="none"
    assert str(Nope()) == '<div class="none"></div>'
    assert str(Nope("hello")) == '<div class="none">hello</div>'
    assert str(Nope("hello", klass='other') ) == '<div class="other">hello</div>'

    class Nope(Tag):
        tag="none"
    assert str(Nope()) == '<none class="nope"></none>'
    assert str(Nope("hello")) == '<none class="nope">hello</none>'
    assert str(Nope("hello", klass='other') ) == '<none class="other">hello</none>'

    class Nope(Tag):
        tag="none"
        klass="nine"
    assert str(Nope()) == '<none class="nine"></none>'
    assert str(Nope("hello")) == '<none class="nine">hello</none>'
    assert str(Nope("hello", klass='other') ) == '<none class="other">hello</none>'

def test_DTag():
    class My(DTag):
        pass
    m=My()
    assert m._tag is None
    assert m.build() is None
    assert m.render() is None
    id=m.id
    assert id
    assert m.getInstance(id) == m

test_ReactiveProp()
test_Tag()
test_Tag_id()
test_Tag_class()
test_DTag()