--
-- PostgreSQL database dump
--

-- Dumped from database version 14.15 (Ubuntu 14.15-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.15 (Ubuntu 14.15-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: product_types; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.product_types (
    id integer NOT NULL,
    type_name character varying(100) NOT NULL
);


--
-- Name: product_types_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.product_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: product_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.product_types_id_seq OWNED BY public.product_types.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.products (
    id integer NOT NULL,
    product_name character varying(255) NOT NULL,
    type_id integer NOT NULL,
    price numeric(10,2) NOT NULL
);


--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: product_types id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.product_types ALTER COLUMN id SET DEFAULT nextval('public.product_types_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Data for Name: product_types; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.product_types (id, type_name) FROM stdin;
1	Пицца
2	Закуска
3	Напиток
4	Десерт
5	Добавка
6	Сувенир
7	Прочее
8	Подарочная карта
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.products (id, product_name, type_id, price) FROM stdin;
12	Додстер	2	150.00
13	Картофель из печи	2	180.00
14	Добрый Кола Small	3	80.00
16	Маффин Три шоколада	4	120.00
17	Коктейль Шоколадный (фризер) 0.3	3	130.00
20	Добрый Лайм-Лимон 0.5	3	90.00
21	Морс Вишня 0.45	3	70.00
22	Морс Черная смородина 0.45	3	70.00
24	Сырный соус Додо	5	30.00
25	Чесночный соус	5	30.00
27	Молоко для 0.4	3	50.00
28	Гель-антисептик для рук	7	200.00
31	Карамельное яблоко молочный коктейль	3	140.00
32	Банановый коктейль 0.3	3	110.00
33	Макарон манго-маракуйя	4	100.00
34	Тирамису NEW	4	160.00
35	Шоколадный кукис NEW	4	90.00
36	Фондан	4	130.00
37	Чизкейк Банановый с шоколадным печеньем	4	170.00
38	Сырники с малиновым вареньем	4	120.00
39	Мороженое в стаканчике с манго и маракуйей	4	150.00
40	Мороженое в стаканчике с клубникой	4	140.00
41	Мороженое в стаканчике без топпинга	4	100.00
42	Мороженое в стаканчике с шоколадом	4	130.00
43	Мороженое в стаканчике с банановым топпингом	4	140.00
44	Кокосовый молочный коктейль	3	120.00
45	Коктейль Классический 0.3	3	100.00
46	Коктейль Клубничный 0.3	3	110.00
47	Коктейль с Орео 0.3	3	120.00
48	Айс Капучино (NEW) 0.3	3	130.00
49	Кофе Капучино 0.4	3	150.00
50	Кофе Латте 0.4	3	150.00
51	Кофе Американо 0.3	3	120.00
52	Кофе Кокосовый латте 0.4	3	160.00
53	Кофе Карамельный Капучино 0.3	3	140.00
54	Кофе Ореховый латте 0.4	3	170.00
55	Вода БонаАква негазированная 0.5	3	50.00
56	Rich Tea Зеленый 0.5	3	80.00
57	Rich Tea Черный с лимоном 0.5	3	80.00
58	Rich Tea Зеленый с манго 0.5	3	90.00
59	Сок Rich Апельсин 0.3	3	70.00
60	Сок Rich Яблоко 0.3	3	70.00
61	Сок Rich Вишня 0.3	3	80.00
62	Детский сок “Добрый” Яблоко 0.2	3	60.00
63	Детский сок “Добрый” Мультифрукт 0.2	3	60.00
64	Какао 0.3	3	100.00
65	Цитрусовый чай с имбирем Big	3	120.00
66	Зеленый чай NEW сенча Big	3	110.00
67	Черный чай с чабрецом Big	3	100.00
68	Таежный чай 0.4	3	80.00
69	Магнит на холодильник «Хочу пиццу»	6	250.00
70	Электронная подарочная Додо–карта Big	8	1000.00
71	Подарочный сертификат 1000 ₽ (локальный маркетинг)	8	1000.00
72	Додо Книга	6	500.00
73	Додо Раскраска	6	300.00
74	Набор для выращивания «Смешарики»	6	400.00
75	Фартук «Pizza is my Credodo»	6	600.00
76	Фартук «We make pizza to open the world»	6	600.00
77	Додо Колпак	6	200.00
78	Многоразовая маска	7	150.00
79	Гель-антисептик для рук Antiseptane	7	200.00
80	Листовка с акцией	7	10.00
81	Открытка «День рождения»	7	50.00
82	Маргарита Small	1	315.00
83	Маргарита Medium	1	405.00
84	Маргарита Large	1	495.00
85	Овощи и грибы Small	1	294.00
86	Овощи и грибы Medium	1	378.00
87	Овощи и грибы Large	1	462.00
88	Пепперони Small	1	336.00
89	Пепперони Medium	1	432.00
90	Пепперони Large	1	528.00
91	Четыре сезона Small	1	350.00
92	Четыре сезона Medium	1	450.00
93	Четыре сезона Large	1	550.00
94	Аррива! Small	1	329.00
95	Аррива! Medium	1	423.00
96	Аррива! Large	1	517.00
97	Бургер-пицца Small	1	364.00
98	Бургер-пицца Medium	1	468.00
99	Бургер-пицца Large	1	572.00
100	Ветчина и грибы Small	1	322.00
101	Ветчина и грибы Medium	1	414.00
102	Ветчина и грибы Large	1	506.00
103	Ветчина и сыр Small	1	308.00
104	Ветчина и сыр Medium	1	396.00
105	Ветчина и сыр Large	1	484.00
106	Гавайская с альфредо Small	1	343.00
107	Гавайская с альфредо Medium	1	441.00
108	Гавайская с альфредо Large	1	539.00
109	Двойной цыпленок Small	1	357.00
110	Двойной цыпленок Medium	1	459.00
111	Двойной цыпленок Large	1	561.00
112	Сырная Small	1	245.00
113	Сырная Medium	1	315.00
114	Сырная Large	1	385.00
115	Диабло Small	1	301.00
116	Диабло Medium	1	387.00
117	Диабло Large	1	473.00
118	Чоризо фреш Small	1	329.00
119	Чоризо фреш Medium	1	423.00
120	Чоризо фреш Large	1	517.00
121	Пепперони Фреш Small	1	336.00
122	Пепперони Фреш Medium	1	432.00
123	Пепперони Фреш Large	1	528.00
124	Карбонара Small	1	455.00
125	Карбонара Medium	1	585.00
126	Карбонара Large	1	715.00
127	Кус Мясо и овощи Римская Small	1	385.00
128	Кус Мясо и овощи Римская Medium	1	495.00
129	Кус Мясо и овощи Римская Large	1	605.00
130	Додо Микс Small	1	490.00
131	Додо Микс Medium	1	630.00
132	Додо Микс Large	1	770.00
133	Миксик Small	1	266.00
134	Миксик Medium	1	342.00
135	Миксик Large	1	418.00
\.


--
-- Name: product_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.product_types_id_seq', 8, true);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.products_id_seq', 135, true);


--
-- Name: product_types product_types_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.product_types
    ADD CONSTRAINT product_types_pkey PRIMARY KEY (id);


--
-- Name: product_types product_types_type_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.product_types
    ADD CONSTRAINT product_types_type_name_key UNIQUE (type_name);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: products products_product_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_product_name_key UNIQUE (product_name);


--
-- Name: products products_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.product_types(id);


--
-- PostgreSQL database dump complete
--

