import sympy

def bissec(func, xe, xd, eps, rmax): #func = string funcao / xe e xd = [a,b] inicial / eps = epsilon / rmax = maximo de repeticoes
    x = sympy.symbols('x')
    func_py = sympy.sympify(func)
    fx = sympy.lambdify(x, func_py)
    dfx = sympy.lambdify(x, sympy.diff(func_py,x))
    a = xe
    b = xd
    xm = (a+b)/2
    fxm = fx(xm)
    iter = 0
    if( ( (dfx(a) >= 0 and dfx(b) >= 0) or (dfx(a) < 0 and dfx(b) < 0) ) and ( (fx(a)*fx(b))<0 ) ):
        while(abs(fxm) > eps and rmax > 0):
            xm = (a+b)/2
            fxm= fx(xm)
            print(f'[ {a:.6f} , {b:.6f} ] | xm = {xm:.6f} | f(xm) = {fxm:.6f} | diferença de f(x) e epsilon = {abs(fxm-eps):.6f}')
            if( ( fx(a)*fxm ) < 0):
                b=xm
            else:
                a=xm
            iter+=1
            rmax-=1
        print(f'x = {xm:.6f} | f(x) = {fxm:.6f} | {iter} iterações!')
        return xm
    return

def fp(func, xe, xd, eps, rmax): #func = string funcao / xe e xd = [a,b] inicial / eps = epsilon / rmax = maximo de repeticoes
    x = sympy.symbols('x')
    func_py = sympy.sympify(func)
    fx = sympy.lambdify(x, func_py)
    dfx = sympy.lambdify(x, sympy.diff(func_py,x))
    a = xe
    b = xd
    fa = fx(a)
    fb = fx(b)
    xm = ( (a*fb-b*fa)/(fb-fa) )
    fxm= fx(xm)
    iter = 0
    while(abs(fxm) > eps and rmax > 0):
        fa = fx(a)
        fb = fx(b)
        xm = ( (a*fb-b*fa)/(fb-fa) )
        fxm= fx(xm)
        print(f'[ {a:.6f} , {b:.6f} ] | xm = {xm:.6f} | f(xm) = {fxm:.6f} | diferença de f(x) e epsilon = {abs(fxm-eps):.6f}')
        if( ( fx(a)*fxm ) < 0):
            b=xm
        else:
            a=xm
        iter+=1
        rmax-=1
    print(f'x = {xm:.6f} | f(x) = {fxm:.6f} | {iter} iterações!')
    return xm

def newton(func, xe, eps, rmax): #func = string funcao / xe = x estimado / eps = epsilon / rmax = maximo de repeticoes
    x = sympy.symbols('x')
    func_py = sympy.sympify(func)
    fx = sympy.lambdify(x, func_py)
    dfx = sympy.lambdify(x, sympy.diff(func_py,x))
    x0 = xe
    fxn = 10
    iter = 0
    while(abs(fxn) > eps and rmax > 0):
        xn = x0-( fx(x0)/dfx(x0) )
        fxn = fx(xn)
        print(f'x{iter} = {x0:.6f} | x{iter+1} = {xn:.6f} | f(x{iter+1}) = {fxn:.6f} | diferença de f(x{iter+1}) e epsilon = {abs(fxn-eps):.6f}')
        x0 = xn
        iter+=1
        rmax-=1
    print(f'x{iter} = {x0:.6f} | f(x{iter}) = {fxn:.6f} | {iter} iterações!')
    return x0

def secante(func, x0, x1, eps, rmax): #func = string funcao / x0 e x1 = estimativas iniciais / eps = epsilon / rmax = maximo de repeticoes
    x = sympy.symbols('x')
    func_py = sympy.sympify(func)
    fx = sympy.lambdify(x, func_py)
    dfx = sympy.lambdify(x, sympy.diff(func_py,x))
    a = x0
    b = x1
    fxm = 10
    iter = 0
    while(abs(fxm) > eps and rmax > 0):
        fxa = fx(a)
        fxb = fx(b)
        xm = ( (a*fxb-b*fxa)/(fxb-fxa) )
        fxm = fx(xm)
        print(f'x{iter} = {a:.6f} | x{iter+1} = {b:.6f} | x{iter+2} = {xm:.6f} | f(x{iter+2}) = {fxm:.6f} | diferença de f(x{iter+2}) e epsilon = {abs(fxm-eps):.6f}')
        a = b
        b = xm
        iter+=1
        rmax-=1
    print(f'x{iter+1} = {b:.6f} | f(x{iter+1}) = {fxm:.6f} | {iter} iterações!')
    return b

bissec("x^3-x-1",1,2,0.0002,20)